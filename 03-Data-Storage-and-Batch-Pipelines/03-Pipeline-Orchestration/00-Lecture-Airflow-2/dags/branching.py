from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import BranchPythonOperator

import random
import pendulum


def branch_func():
    random_number = random.random()
    if random_number >= 0.5:
        return "continue"
    return "stop"


with DAG(
    "branching_dag",
    start_date=pendulum.today("UTC").add(days=-6),
    schedule_interval="@daily",
) as dag:
    # Tasks
    branch_task = BranchPythonOperator(task_id="branch", python_callable=branch_func)

    continue_task = EmptyOperator(task_id="continue")
    stop_task = EmptyOperator(task_id="stop")

    after_continue = EmptyOperator(task_id="after_continue")

    # Graph
    branch_task >> [continue_task, stop_task]
    continue_task >> after_continue
