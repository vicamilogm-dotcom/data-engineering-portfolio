from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator

import pendulum


with DAG(
    "parent_dag",
    start_date=pendulum.today("UTC").add(days=-2),
    schedule_interval="@daily",
    catchup=False,
) as dag:
    # Tasks
    do_nothing_task = EmptyOperator(task_id="do_nothing")

    do_something_task = BashOperator(task_id="do_something", bash_command="echo 1")

    # Graph
    do_nothing_task >> do_something_task
