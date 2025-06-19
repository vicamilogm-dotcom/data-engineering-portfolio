from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
import pendulum

with DAG(
    "create_table_example",
    description="An example dag to create a table",
    schedule_interval="@daily",
    start_date=pendulum.datetime(2025, 6, 15, tz="UTC"),  # Update to something recent
    catchup=False,
) as dag:
    create_example_table_task = SQLExecuteQueryOperator(
        task_id="create_example_table",
        conn_id="sqlite_connection",
        sql="CREATE TABLE IF NOT EXISTS examples (example VARCHAR);",
    )

    # Execution graph
    create_example_table_task
