from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.sqlite.hooks.sqlite import SqliteHook

import pendulum


def list_tables():
    hook = SqliteHook(sqlite_conn_id="sqlite_connection")
    dags = hook.get_records("SELECT * FROM dag;")
    for dag in dags:
        print(dag)


with DAG(
    "hook_example",
    start_date=pendulum.datetime(2025, 6, 15, tz="UTC"),  # Update to something recent
    schedule_interval="@daily",
    catchup=False,
) as dag:
    list_tables_task = PythonOperator(
        task_id="list_tables",
        python_callable=list_tables,
    )

    list_tables_task
