import os

from airflow.hooks.sqlite_hook import SqliteHook
from airflow.models import DagBag
from airflow.models.taskinstance import TaskInstance
from airflow.utils.state import DagRunState
from airflow.utils.types import DagRunType
from pendulum.datetime import DateTime
from pendulum.tz.timezone import Timezone

DAG_BAG = os.path.join(os.path.dirname(__file__), "../dags")
os.environ["AIRFLOW_HOME"] = "/app/airflow"


class TestLoadDag:
    dagbag = DagBag(dag_folder=DAG_BAG, include_examples=False)

    def test_dag_config(self):
        dag = self.dagbag.get_dag(dag_id="load")

        assert dag.schedule_interval == "@monthly"
        assert dag.catchup is True
        assert dag.default_args == {"depends_on_past": True}
        assert dag.start_date == DateTime(2021, 6, 1, 0, 0, 0, tzinfo=Timezone("UTC"))
        assert dag.end_date == DateTime(2021, 12, 31, 0, 0, 0, tzinfo=Timezone("UTC"))

    def test_tasks(self):
        dag = self.dagbag.get_dag(dag_id="load")

        assert list(map(lambda task: task.task_id, dag.tasks)) == [
            "transform_sensor",
            "upload_local_file_to_gcs",
            "create_dataset",
            "create_table",
            "remove_existing_data",
            "load_to_bigquery",
        ]

    def test_transform_sensor_task(self):
        dag = self.dagbag.get_dag(dag_id="load")
        task = dag.get_task("transform_sensor")

        assert task.__class__.__name__ == "ExternalTaskSensor"
        assert task.external_dag_id == "transform"
        assert task.allowed_states == ["success"]
        assert task.poke_interval == 10
        assert task.timeout == 60 * 10
        assert list(map(lambda task: task.task_id, task.upstream_list)) == []
        assert list(map(lambda task: task.task_id, task.downstream_list)) == [
            "upload_local_file_to_gcs"
        ]

    def test_upload_local_file_to_gcs_task(self):
        dag = self.dagbag.get_dag(dag_id="load")
        task = dag.get_task("upload_local_file_to_gcs")

        assert task.__class__.__name__ == "LocalFilesystemToGCSOperator"

        hook = SqliteHook(sqlite_conn_id="sqlite_connection")
        start_date = DateTime(2021, 6, 1, 0, 0, 0, tzinfo=Timezone("UTC"))

        for month in range(6, 7):
            hook.run("DELETE FROM dag_run")
            execution_date = DateTime(2021, month, 1, 0, 0, 0, tzinfo=Timezone("UTC"))

            dagrun = dag.create_dagrun(
                state=DagRunState.RUNNING,
                execution_date=execution_date,
                start_date=start_date,
                run_type=DagRunType.MANUAL,
                data_interval=(execution_date, start_date),
            )

            ti = TaskInstance(task, run_id=dagrun.run_id)
            ti.dry_run()

            assert task.gcp_conn_id == "google_cloud_connection"
            assert (
                ti.task.src
                == f"/app/airflow/data/silver/yellow_tripdata_2021-0{month}.csv"
            )
            assert ti.task.dst == f"yellow_tripdata_2021-0{month}.csv"
            assert ti.task.bucket is not None

        assert list(map(lambda task: task.task_id, task.upstream_list)) == [
            "transform_sensor"
        ]
        assert list(map(lambda task: task.task_id, task.downstream_list)) == [
            "create_dataset"
        ]

    def test_create_dataset_task(self):
        dag = self.dagbag.get_dag(dag_id="load")
        task = dag.get_task("create_dataset")

        assert task.__class__.__name__ == "BigQueryCreateEmptyDatasetOperator"
        assert task.gcp_conn_id == "google_cloud_connection"
        assert task.dataset_id.endswith("gold")

        assert list(map(lambda task: task.task_id, task.upstream_list)) == [
            "upload_local_file_to_gcs"
        ]
        assert list(map(lambda task: task.task_id, task.downstream_list)) == [
            "create_table"
        ]

    def test_create_table_task(self):
        dag = self.dagbag.get_dag(dag_id="load")
        task = dag.get_task("create_table")

        assert task.__class__.__name__ == "BigQueryCreateEmptyTableOperator"
        assert task.gcp_conn_id == "google_cloud_connection"
        assert task.dataset_id.endswith("gold")
        assert task.table_id == "trips"
        assert task.schema_fields[0]["name"] == "date"
        assert task.schema_fields[0]["type"].lower() == "string"
        assert task.schema_fields[1]["name"] == "trip_distance"
        assert task.schema_fields[1]["type"].lower() == "float"
        assert task.schema_fields[2]["name"] == "total_amount"
        assert task.schema_fields[2]["type"].lower() == "float"

        assert list(map(lambda task: task.task_id, task.upstream_list)) == [
            "create_dataset"
        ]
        assert list(map(lambda task: task.task_id, task.downstream_list)) == [
            "remove_existing_data"
        ]

    def test_remove_existing_data_task(self):
        dag = self.dagbag.get_dag(dag_id="load")
        task = dag.get_task("remove_existing_data")

        assert task.__class__.__name__ == "BigQueryInsertJobOperator"
        assert task.gcp_conn_id == "google_cloud_connection"

        hook = SqliteHook(sqlite_conn_id="sqlite_connection")
        start_date = DateTime(2021, 6, 1, 0, 0, 0, tzinfo=Timezone("UTC"))

        for month in range(6, 7):
            hook.run("DELETE FROM dag_run")
            execution_date = DateTime(2021, month, 1, 0, 0, 0, tzinfo=Timezone("UTC"))

            dagrun = dag.create_dagrun(
                state=DagRunState.RUNNING,
                execution_date=execution_date,
                start_date=start_date,
                run_type=DagRunType.MANUAL,
                data_interval=(execution_date, start_date),
            )

            ti = TaskInstance(task, run_id=dagrun.run_id)
            ti.dry_run()

            assert ti.task.gcp_conn_id == "google_cloud_connection"
            assert (
                ti.task.configuration["query"]["query"]
                .lower()
                .startswith("delete from ")
            )
            assert (
                ti.task.configuration["query"]["query"]
                .lower()
                .endswith(f"gold.trips where date = '2021-0{month}'")
            )

        assert list(map(lambda task: task.task_id, task.upstream_list)) == [
            "create_table"
        ]
        assert list(map(lambda task: task.task_id, task.downstream_list)) == [
            "load_to_bigquery"
        ]

    def test_load_to_bigquery_task(self):
        dag = self.dagbag.get_dag(dag_id="load")
        task = dag.get_task("load_to_bigquery")

        assert task.__class__.__name__ == "GCSToBigQueryOperator"

        hook = SqliteHook(sqlite_conn_id="sqlite_connection")
        start_date = DateTime(2021, 6, 1, 0, 0, 0, tzinfo=Timezone("UTC"))

        for month in range(6, 7):
            hook.run("DELETE FROM dag_run")
            execution_date = DateTime(2021, month, 1, 0, 0, 0, tzinfo=Timezone("UTC"))

            dagrun = dag.create_dagrun(
                state=DagRunState.RUNNING,
                execution_date=execution_date,
                start_date=start_date,
                run_type=DagRunType.MANUAL,
                data_interval=(execution_date, start_date),
            )

            ti = TaskInstance(task, run_id=dagrun.run_id)
            ti.dry_run()

            assert ti.task.gcp_conn_id == "google_cloud_connection"
            assert ti.task.bucket.endswith("silver")
            assert ti.task.source_objects == f"yellow_tripdata_2021-0{month}.csv"
            assert ti.task.destination_project_dataset_table.endswith("gold.trips")

        assert list(map(lambda task: task.task_id, task.upstream_list)) == [
            "remove_existing_data"
        ]
        assert list(map(lambda task: task.task_id, task.downstream_list)) == []
