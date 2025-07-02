from airflow import DAG
from airflow.operators.empty import EmptyOperator

import pendulum

with DAG(
    "complex",
    start_date=pendulum.today("UTC").add(days=-2),
    schedule_interval="@daily",
    catchup=False,
) as dag:
    # Tasks
    start_1_task = EmptyOperator(task_id="start_1")
    start_2_task = EmptyOperator(task_id="start_2")

    after_start_1_task = EmptyOperator(task_id="after_start_1")
    after_start_2_task = EmptyOperator(task_id="after_start_2")

    first_branch_after_start_1_task = EmptyOperator(
        task_id="first_branch_after_start_1"
    )
    second_branch_after_start_1_task = EmptyOperator(
        task_id="second_branch_after_start_1"
    )

    after_first_branch_task = EmptyOperator(task_id="after_first_branch")

    stop_task = EmptyOperator(task_id="stop")

    # Graph
    (
        start_1_task
        >> after_start_1_task
        >> [first_branch_after_start_1_task, second_branch_after_start_1_task]
    )

    first_branch_after_start_1_task >> after_first_branch_task >> stop_task
    second_branch_after_start_1_task >> stop_task

    start_2_task >> after_start_2_task >> stop_task
