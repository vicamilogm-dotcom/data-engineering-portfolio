import os.path

# from airflow.hooks.sqlite_hook import SqliteHook
from airflow.providers.sqlite.hooks.sqlite import SqliteHook
from airflow.models import DagBag
from airflow.models.taskinstance import TaskInstance
from airflow.utils.state import DagRunState
from airflow.utils.types import DagRunType
from pendulum.datetime import DateTime
from pendulum.tz.timezone import Timezone

DAG_BAG = os.path.join(os.path.dirname(__file__), "../dags")

# Set this variable temporarily back to student-config but without affecting airflow test configuration.
os.environ["AIRFLOW_HOME"] = "/app/airflow"


class TestTasksConfigs:
    dagbag = DagBag(dag_folder=DAG_BAG, include_examples=False)
    hook = SqliteHook(sqlite_conn_id="sqlite_connection")
    joke_file_prefix = "/app/airflow/data/bronze/joke_"
    swedified_joke_file_prefix = "/app/airflow/data/silver/swedified_joke_"
    start_date = DateTime(2022, 1, 1, 0, 0, 0, tzinfo=Timezone("UTC"))

    def test_tasks(self):
        assert self.dagbag.import_errors == {}, self.dagbag.import_errors
        dag = self.dagbag.get_dag(dag_id="local_etl")
        assert list(map(lambda task: task.task_id, dag.tasks)) == [
            "create_swedified_jokes_table",
            "extract",
            "transform",
            "load",
        ]

    def test_create_swedified_jokes_task(self):
        assert self.dagbag.import_errors == {}, self.dagbag.import_errors
        dag = self.dagbag.get_dag(dag_id="local_etl")
        task = dag.get_task("create_swedified_jokes_table")

        assert task.__class__.__name__ == "PostgresOperator"
        ## TOO STRICT
        # assert (
        #     task.sql
        #     == """CREATE TABLE IF NOT EXISTS swedified_jokes (
        #         id SERIAL PRIMARY KEY,
        #         joke VARCHAR NOT NULL,
        #         swedified_joke VARCHAR NOT NULL
        #     );"""
        # )
        assert task.conn_id == "postgres_connection"

        assert list(map(lambda task: task.task_id, task.upstream_list)) == []
        assert list(map(lambda task: task.task_id, task.downstream_list)) == ["extract"]

    def test_extract_task(self):
        assert self.dagbag.import_errors == {}, self.dagbag.import_errors
        dag = self.dagbag.get_dag(dag_id="local_etl")
        task = dag.get_task("extract")
        assert task.__class__.__name__ == "BashOperator"
        data_url = "https://api.chucknorris.io/jokes/random"

        for day in range(1, 2):
            self.hook.run("DELETE FROM dag_run")
            execution_date = DateTime(2022, 1, day, 0, 0, 0, tzinfo=Timezone("UTC"))

            dagrun = dag.create_dagrun(
                state=DagRunState.RUNNING,
                execution_date=execution_date,
                start_date=self.start_date,
                run_type=DagRunType.MANUAL,
                data_interval=(execution_date, self.start_date),
            )

            ti = TaskInstance(task, run_id=dagrun.run_id)
            ti.dry_run()

            assert (
                ti.task.bash_command
                == f"curl {data_url} > {self.joke_file_prefix}2022010{day}.json"
            )

        assert list(map(lambda task: task.task_id, task.upstream_list)) == [
            "create_swedified_jokes_table"
        ]
        assert list(map(lambda task: task.task_id, task.downstream_list)) == [
            "transform"
        ]

    def test_transform_task(self):
        assert self.dagbag.import_errors == {}, self.dagbag.import_errors
        dag = self.dagbag.get_dag(dag_id="local_etl")
        task = dag.get_task("transform")

        assert task.__class__.__name__ == "PythonOperator"
        assert task.python_callable.__name__ == "transform"
        for day in range(1, 2):
            self.hook.run("DELETE FROM dag_run")
            execution_date = DateTime(2022, 1, day, 0, 0, 0, tzinfo=Timezone("UTC"))

            dagrun = dag.create_dagrun(
                state=DagRunState.RUNNING,
                execution_date=execution_date,
                start_date=self.start_date,
                run_type=DagRunType.MANUAL,
                data_interval=(execution_date, self.start_date),
            )

            ti = TaskInstance(task, run_id=dagrun.run_id)
            ti.dry_run()

            assert ti.task.op_kwargs == {
                "joke_file": f"{self.joke_file_prefix}2022010{day}.json",
                "swedified_joke_file": f"{self.swedified_joke_file_prefix}2022010{day}.json",
            }

        assert list(map(lambda task: task.task_id, task.upstream_list)) == ["extract"]
        assert list(map(lambda task: task.task_id, task.downstream_list)) == ["load"]

    def test_load_task(self):
        assert self.dagbag.import_errors == {}, self.dagbag.import_errors
        dag = self.dagbag.get_dag(dag_id="local_etl")
        task = dag.get_task("load")

        assert task.__class__.__name__ == "PythonOperator"
        assert task.python_callable.__name__ == "load"
        assert list(task.op_kwargs.keys()) == ["swedified_joke_file", "hook"]
        for day in range(1, 2):
            self.hook.run("DELETE FROM dag_run")
            execution_date = DateTime(2022, 1, day, 0, 0, 0, tzinfo=Timezone("UTC"))

            dagrun = dag.create_dagrun(
                state=DagRunState.RUNNING,
                execution_date=execution_date,
                start_date=self.start_date,
                run_type=DagRunType.MANUAL,
                data_interval=(execution_date, self.start_date),
            )

            ti = TaskInstance(task, run_id=dagrun.run_id)
            ti.dry_run()

            assert (
                ti.task.op_kwargs["swedified_joke_file"]
                == f"{self.swedified_joke_file_prefix}2022010{day}.json"
            )
            assert ti.task.op_kwargs["hook"].__class__.__name__ == "PostgresHook"
            assert ti.task.op_kwargs["hook"].postgres_conn_id == "postgres_connection"

        assert list(map(lambda task: task.task_id, task.upstream_list)) == ["transform"]
        assert list(map(lambda task: task.task_id, task.downstream_list)) == []
