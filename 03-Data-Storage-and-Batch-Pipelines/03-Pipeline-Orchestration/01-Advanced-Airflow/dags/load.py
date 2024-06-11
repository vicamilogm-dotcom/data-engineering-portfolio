import os
from datetime import datetime

from airflow import DAG

from airflow.sensors.external_task import ExternalTaskSensor

from airflow.providers.google.cloud.operators.bigquery import (
    BigQueryCreateEmptyDatasetOperator,
    BigQueryCreateEmptyTableOperator,
    BigQueryInsertJobOperator,
)
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import (
    GCSToBigQueryOperator,
)

from airflow.providers.google.cloud.transfers.local_to_gcs import (
    LocalFilesystemToGCSOperator,
)

AIRFLOW_HOME = os.getenv("AIRFLOW_HOME")

with DAG(
    "load",
    default_args={"depends_on_past": True},
    start_date=datetime(2021, 6, 1),
    end_date=datetime(2021, 12, 31),
    schedule_interval="@monthly",
) as dag:
    date = "{{ ds[:7] }}"
    filtered_data_file = f"{AIRFLOW_HOME}/data/silver/yellow_tripdata_{date}.csv"
    wait_for_transform_task = ExternalTaskSensor(
        task_id="transform_sensor",
        # YOUR CODE HERE
    )

    upload_local_file_to_gcs_task = LocalFilesystemToGCSOperator(
        task_id="upload_local_file_to_gcs",
        # YOUR CODE HERE
    )

    create_dataset_task = BigQueryCreateEmptyDatasetOperator(
        task_id="create_dataset",
        # YOUR CODE HERE
    )

    create_table_task = BigQueryCreateEmptyTableOperator(
        task_id="create_table",
        # YOUR CODE HERE
    )

    remove_existing_data_task = BigQueryInsertJobOperator(
        task_id="remove_existing_data",
        # YOUR CODE HERE
    )

    load_to_bigquery_task = GCSToBigQueryOperator(
        task_id="load_to_bigquery",
        # YOUR CODE HERE
    )

    # Organise your tasks hierachy here
    pass  # YOUR CODE HERE
