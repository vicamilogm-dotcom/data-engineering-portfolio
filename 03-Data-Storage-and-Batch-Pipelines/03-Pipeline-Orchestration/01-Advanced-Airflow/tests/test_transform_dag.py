import os

import pandas as pd
from airflow.hooks.sqlite_hook import SqliteHook
from airflow.models import DagBag
from airflow.models.taskinstance import TaskInstance
from airflow.utils.state import DagRunState
from airflow.utils.types import DagRunType
from dags import transform
from pendulum.datetime import DateTime
from pendulum.tz.timezone import Timezone

DAG_BAG = os.path.join(os.path.dirname(__file__), "../dags")
COLUMNS_TO_KEEP = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime",
    "total_amount",
    "trip_distance",
]
os.environ["AIRFLOW_HOME"] = "/app/airflow"


class TestTransformDag:
    hook = SqliteHook(sqlite_conn_id="sqlite_connection")
    start_date = DateTime(2021, 6, 1, 0, 0, 0, tzinfo=Timezone("UTC"))
    dagbag = DagBag(dag_folder=DAG_BAG, include_examples=False)

    def test_dag_config(self):
        dag = self.dagbag.get_dag(dag_id="transform")
        assert dag.schedule_interval == "@monthly"

        assert dag.catchup is True
        assert dag.default_args == {"depends_on_past": True}
        assert dag.start_date == self.start_date
        assert dag.end_date == DateTime(2021, 12, 31, 0, 0, 0, tzinfo=Timezone("UTC"))

    def test_tasks(self):
        dag = self.dagbag.get_dag(dag_id="transform")

        assert list(map(lambda task: task.task_id, dag.tasks)) == [
            "extract_sensor",
            "is_month_odd",
            "filter_long_trips",
            "filter_expensive_trips",
            "end",
        ]

        extract_sensor_task = dag.get_task("extract_sensor")

        assert extract_sensor_task.__class__.__name__ == "ExternalTaskSensor"
        assert extract_sensor_task.external_dag_id == "extract"
        assert extract_sensor_task.allowed_states == ["success"]
        assert extract_sensor_task.poke_interval == 10
        assert extract_sensor_task.timeout == 60 * 10
        assert (
            list(map(lambda task: task.task_id, extract_sensor_task.upstream_list))
            == []
        )
        assert list(
            map(lambda task: task.task_id, extract_sensor_task.downstream_list)
        ) == ["is_month_odd"]

        is_month_odd_task = dag.get_task("is_month_odd")

        assert is_month_odd_task.__class__.__name__ == "BranchPythonOperator"
        assert is_month_odd_task.python_callable.__name__ == "is_month_odd"
        assert list(
            map(lambda task: task.task_id, is_month_odd_task.upstream_list)
        ) == ["extract_sensor"]
        assert set(
            map(lambda task: task.task_id, is_month_odd_task.downstream_list)
        ) == {"filter_long_trips", "filter_expensive_trips"}

        filter_long_trips_task = dag.get_task("filter_long_trips")

        assert filter_long_trips_task.__class__.__name__ == "PythonOperator"
        assert filter_long_trips_task.python_callable.__name__ == "filter_long_trips"
        assert list(
            map(lambda task: task.task_id, filter_long_trips_task.upstream_list)
        ) == ["is_month_odd"]
        assert list(
            map(lambda task: task.task_id, filter_long_trips_task.downstream_list)
        ) == ["end"]

        filter_expensive_trips_task = dag.get_task("filter_expensive_trips")

        assert filter_expensive_trips_task.__class__.__name__ == "PythonOperator"
        assert (
            filter_expensive_trips_task.python_callable.__name__
            == "filter_expensive_trips"
        )
        assert list(
            map(lambda task: task.task_id, filter_expensive_trips_task.upstream_list)
        ) == ["is_month_odd"]
        assert list(
            map(lambda task: task.task_id, filter_expensive_trips_task.downstream_list)
        ) == ["end"]

        end_task = dag.get_task("end")

        assert end_task.__class__.__name__ == "EmptyOperator"
        assert end_task.trigger_rule == "one_success"

        for month in range(6, 7):
            self.hook.run("DELETE FROM dag_run")
            execution_date = DateTime(2021, month, 1, 0, 0, 0, tzinfo=Timezone("UTC"))

            dagrun = dag.create_dagrun(
                state=DagRunState.RUNNING,
                execution_date=execution_date,
                start_date=self.start_date,
                run_type=DagRunType.MANUAL,
                data_interval=(execution_date, self.start_date),
            )

            ti_is_month_odd = TaskInstance(is_month_odd_task, run_id=dagrun.run_id)
            ti_is_month_odd.dry_run()
            assert ti_is_month_odd.task.op_kwargs == {"date": f"2021-0{month}"}

            ti_filter_long_trips = TaskInstance(
                filter_long_trips_task, run_id=dagrun.run_id
            )
            ti_filter_long_trips.dry_run()

            assert ti_filter_long_trips.task.op_kwargs == {
                "bronze_file": f"/app/airflow/data/bronze/yellow_tripdata_2021-0{month}.parquet",
                "silver_file": f"/app/airflow/data/silver/yellow_tripdata_2021-0{month}.csv",
                "date": f"2021-0{month}",
                "distance": 150,
            }

            filter_expensive_trips_ti = TaskInstance(
                filter_expensive_trips_task, run_id=dagrun.run_id
            )
            filter_expensive_trips_ti.dry_run()

            assert filter_expensive_trips_ti.task.op_kwargs == {
                "bronze_file": f"/app/airflow/data/bronze/yellow_tripdata_2021-0{month}.parquet",
                "silver_file": f"/app/airflow/data/silver/yellow_tripdata_2021-0{month}.csv",
                "date": f"2021-0{month}",
                "amount": 500,
            }


def remove_temp_file(temp_file):
    if os.path.isfile(temp_file):
        os.remove(temp_file)


def assert_dataframe_has_all_values_and_filtered_columns(df, month):
    assert list(df.columns.values) == ["date", "trip_distance", "total_amount"]
    assert list(df["date"].values) == [f"2021-0{month}", f"2021-0{month}"]
    assert list(df["trip_distance"].values) == [1, 2]
    assert list(df["total_amount"].values) == [3, 4]


def assert_dataframe_has_second_values_and_filtered_columns(df, month):
    assert list(df.columns.values) == ["date", "trip_distance", "total_amount"]
    assert list(df["date"].values) == [f"2021-0{month}"]
    assert list(df["trip_distance"].values) == [2]
    assert list(df["total_amount"].values) == [4]


def assert_dataframe_has_no_values_and_filtered_columns(df):
    assert list(df.columns.values) == ["date", "trip_distance", "total_amount"]
    assert list(df["date"].values) == []
    assert list(df["trip_distance"].values) == []
    assert list(df["total_amount"].values) == []


def test_is_month_odd():
    assert transform.is_month_odd("2021-06") == "filter_expensive_trips"
    assert transform.is_month_odd("2021-07") == "filter_long_trips"


def test_prepare_data():
    for month in [6, 7]:
        df = transform.prepare_data(
            "tests/data/bronze/dataframe.parquet", f"2021-0{month}"
        )
        assert_dataframe_has_all_values_and_filtered_columns(df, month)


def test_filter_long_trips():
    temp_file = "tests/temp/dataframe.csv"

    for month in [6, 7]:
        remove_temp_file(temp_file)
        transform.filter_long_trips(
            "tests/data/bronze/dataframe.parquet", temp_file, f"2021-0{month}", 0
        )
        df = pd.read_csv(temp_file)
        assert_dataframe_has_all_values_and_filtered_columns(df, month)

        remove_temp_file(temp_file)
        transform.filter_long_trips(
            "tests/data/bronze/dataframe.parquet", temp_file, f"2021-0{month}", 1
        )
        df = pd.read_csv(temp_file)
        assert_dataframe_has_second_values_and_filtered_columns(df, month)

        remove_temp_file(temp_file)
        transform.filter_long_trips(
            "tests/data/bronze/dataframe.parquet", temp_file, f"2021-0{month}", 2
        )
        df = pd.read_csv(temp_file)
        assert_dataframe_has_no_values_and_filtered_columns(df)


def test_filter_expensive_trips():
    temp_file = "tests/temp/dataframe.csv"

    for month in [6, 7]:
        remove_temp_file(temp_file)
        transform.filter_expensive_trips(
            "tests/data/bronze/dataframe.parquet", temp_file, f"2021-0{month}", 2
        )
        df = pd.read_csv(temp_file)
        assert_dataframe_has_all_values_and_filtered_columns(df, month)

        remove_temp_file(temp_file)
        transform.filter_expensive_trips(
            "tests/data/bronze/dataframe.parquet", temp_file, f"2021-0{month}", 3
        )
        df = pd.read_csv(temp_file)
        assert_dataframe_has_second_values_and_filtered_columns(df, month)

        remove_temp_file(temp_file)
        transform.filter_expensive_trips(
            "tests/data/bronze/dataframe.parquet", temp_file, f"2021-0{month}", 4
        )
        df = pd.read_csv(temp_file)
        assert_dataframe_has_no_values_and_filtered_columns(df)
