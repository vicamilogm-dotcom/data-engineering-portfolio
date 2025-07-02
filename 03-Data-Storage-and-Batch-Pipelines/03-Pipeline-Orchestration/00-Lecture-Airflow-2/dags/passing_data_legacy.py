from airflow import DAG
from airflow.operators.python import PythonOperator

import logging
import pendulum


def push_data(**kwargs):
    task_instance = kwargs["ti"]
    task_instance.xcom_push("my_key", "Data from push")


def pull_data(**kwargs):
    task_instance = kwargs["ti"]
    value = task_instance.xcom_pull(task_ids="push", key="my_key")
    logging.info(value)


with DAG(
    "passing_data_legacy",
    start_date=pendulum.today("UTC").add(days=-2),
    schedule_interval="@daily",
    catchup=False,
) as dag:
    # Tasks
    push_task = PythonOperator(
        task_id="push", python_callable=push_data, provide_context=True
    )

    pull_task = PythonOperator(
        task_id="pull", python_callable=pull_data, provide_context=True
    )

    # Graph
    push_task >> pull_task
