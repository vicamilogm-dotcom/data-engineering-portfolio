from airflow import DAG
from airflow.sensors.external_task import ExternalTaskSensor
from airflow.operators.bash import BashOperator

import pendulum


with DAG(
    "child_dag",
    start_date=pendulum.today("UTC").add(days=-2),
    schedule_interval="@daily",
    catchup=False,
) as dag:
    # Tasks
    wait_for_parent_task = ExternalTaskSensor(
        task_id="wait_for_parent",
        external_dag_id="parent_dag",
        external_task_id="do_something",
        timeout=600,
        allowed_states=["success"],
        poke_interval=15,
    )

    print_start = BashOperator(task_id="print_start", bash_command="echo start")

    # Graph
    wait_for_parent_task >> print_start
