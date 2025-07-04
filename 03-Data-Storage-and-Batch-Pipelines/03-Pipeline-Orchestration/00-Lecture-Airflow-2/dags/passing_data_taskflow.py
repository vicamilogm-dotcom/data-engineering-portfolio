from airflow.decorators import task, dag
from airflow.operators.bash import BashOperator

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

    bash_task = BashOperator(task_id="bash_task", bash_command='echo "not taskflow"')

    # Graph
    push_task >> pull_task >> bash_task


dag = my_dag()
