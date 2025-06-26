from airflow import DAG
from airflow.operators.python import PythonOperator
import pendulum


def print_execution_date(date):
    print(date)


with DAG(
    "jinja_example",
    start_date=pendulum.datetime(2025, 1, 1, tz="UTC"), # change to something recent
    schedule_interval="@monthly",
) as dag:
    # Task definition
    print_execution_date_task = PythonOperator(
        task_id="print_execution_date",
        python_callable=print_execution_date,
        op_kwargs=dict(date="{{ ds }}"),
        # op_kwargs={"date": "{{ ds }}"}, # This is equivalent to the above line
    )

    # Execution graph
    print_execution_date_task
