from airflow import DAG
from airflow.operators.empty import EmptyOperator

import pendulum


def create_task(number):
    return EmptyOperator(task_id=f"do_nothing_{number}")


with DAG(
    "programmatic_dag",
    start_date=pendulum.today("UTC").add(days=-2),
    schedule_interval="@daily",
    catchup=False,
) as dag:
    do_nothing_task = EmptyOperator(task_id="do_nothing")

    tasks = []
    for i in range(3):
        tasks.append(create_task(i))

    do_nothing_task >> tasks
