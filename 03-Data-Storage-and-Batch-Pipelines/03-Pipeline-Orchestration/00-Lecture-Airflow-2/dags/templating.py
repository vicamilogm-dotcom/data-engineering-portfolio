from airflow import DAG
from airflow.operators.python import PythonOperator

import pendulum


def print_execution_date(date):
    print(date)


with DAG(
    "templating",
    description="A simple DAG",
    start_date=pendulum.today("UTC").add(days=-2),
    schedule_interval="@daily",
) as dag:
    # Tasks
    print_execution_date_task = PythonOperator(
        task_id="print_execution_date",
        python_callable=print_execution_date,
        op_kwargs={"date": "{{ ds[0] }}"},
    )

    # Graph
    print_execution_date_task
