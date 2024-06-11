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


class TestExtractDag:
    dagbag = DagBag(dag_folder=DAG_BAG, include_examples=False)

    def test_dag_config(self):
        dag = self.dagbag.get_dag(dag_id="extract")
        assert dag.schedule_interval == "@monthly"
        assert dag.catchup is True
        assert dag.default_args == {
            "depends_on_past": True,
        }
        assert dag.start_date == DateTime(2021, 6, 1, 0, 0, 0, tzinfo=Timezone("UTC"))
        assert dag.end_date == DateTime(2021, 12, 31, 0, 0, 0, tzinfo=Timezone("UTC"))

    def test_extract_tasks(self):
        dag = self.dagbag.get_dag(dag_id="extract")
        assert list(map(lambda task: task.task_id, dag.tasks)) == [
            "curl_trip_data",
        ]

    def test_curl_trip_data_task_task(self):
        dag = self.dagbag.get_dag(dag_id="extract")
        task = dag.get_task("curl_trip_data")

        assert task.__class__.__name__ == "BashOperator"

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

            url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-0{month}.parquet"
            filename = f"/app/airflow/data/bronze/yellow_tripdata_2021-0{month}.parquet"
            assert ti.task.bash_command == f"curl {url} > {filename}"
