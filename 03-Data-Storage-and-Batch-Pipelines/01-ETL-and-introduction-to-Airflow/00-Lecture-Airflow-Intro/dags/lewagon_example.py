from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
import pendulum
import time


def my_sleeping_function(time_to_sleep):
    time.sleep(time_to_sleep)


with DAG(
    "lewagon_example",
    description="A simple DAG for Le Wagon",
    schedule_interval="@daily",
    start_date=pendulum.datetime(2025, 6, 15, tz="UTC"),  # Update to something recent
) as dag:
    # Define tasks - order is arbitrary

    run_this_last = EmptyOperator(
        task_id="run_this_last",
    )

    run_this_first = BashOperator(
        task_id="run_this_first",
        bash_command="echo 1",
    )

    for i in range(5):
        task = PythonOperator(
            task_id=f"sleep_for_{i}",
            python_callable=my_sleeping_function,
            op_kwargs={
                "time_to_sleep": i,
            },
        )

        run_this_first >> task

    # Define execution graph

    run_this_first >> run_this_last
