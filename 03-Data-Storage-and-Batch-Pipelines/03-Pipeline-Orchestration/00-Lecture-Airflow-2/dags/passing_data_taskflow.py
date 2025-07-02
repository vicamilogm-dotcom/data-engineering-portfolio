from airflow.decorators import task, dag

import pendulum
import logging


@task
def push_data():
    return "my_value"


@task
def pull_data(data: str):
    logging.info(data)


@dag(
    "passing_data_taskflow",
    start_date=pendulum.today("UTC").add(days=-2),
    schedule_interval="@daily",
    catchup=False,
)
def my_dag():
    # Tasks
    push_task = push_data()
    pull_task = pull_data(push_task)

    # Graph
    push_task >> pull_task


dag = my_dag()
