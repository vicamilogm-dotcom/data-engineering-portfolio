# 🎯 Goals

In this challenge you will build an ETL relatively similar to 020303-Local-ETL, but with more advanced Airflow concepts.

a) Instead of having 3 tasks (E,T,L) in one dag, we'll have 3 DAGs (E,T,L) depending on each other

b) Each tasks will be more complex, making use of
- `Sensor`
- `BranchOperator`
- `Templating`
- `trigger_rule`
- `idempotency`

c) Data flow between clouds:
- `Google Cloud Storage` (your Lake - silver layer)
- `BigQuery` (your Warehouse - gold layer)

🎯 The goal is to have three DAGs running every month that will:
1. **Extract** Download the monthly New York City Taxi (NYC-TLC) [data](https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page) and save it as *parquet* format in your local bronze folder 🥉

2. **Transform** Filter the data based on the month to only keep outliers and save it as CSV in your local silver folder 🥈

3. **Load** the filtered data into both your Lake's silver layer, then into Data Warehouse's gold 🥇 layer


### Setup Instructions

The `Dockerfile` and the `docker-compose.yml` are the same as the ones you used previous airflow day, and we have already prepared the `pyproject.toml` for you.

👉 Just create an `.env` file and set `POSTGRES_PASSWORD` to the value of your choice and you should be able to `docker compose up`

As your three DAGs should have the same config, we already provided them to you. For each of them, you will follow the same process:
- create the required tasks
- test locally by running the Airflow instance and launching your dags
- run the tests

# 1️⃣ "Extract" DAG

As we've already done something similar in previous challenge 020303-Local-ETL, we gave you the code.

The `curl_trip_data` task_id:
- Curls monthly data from a s3 bucket (paths designed like this `https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_YYYY-MM.parquet`)
- Stores it locally on your disk. You should save the parquet file to `/app/airflow/data/bronze/yellow_tripdata_YYYY-MM.parquet`.

Launch your app, open an Airflow instance locally and start your DAG to download the data and make sure that it is appearing in your folder. Then run:

```bash
make test_extract_dag
```

You will see that the tests fake running your DAG on two dates `2021-06-01` and `2021-07-01` to make sure that you correctly use Airflow's variables.

# 2️⃣ "Transform" DAG
Let's build a conditional DAG:

<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/airflow_advanced_transform_dag.png" width=500>

The main goal of this DAG is to read the parquet file you saved in `bronze`, to apply a specific operation based on the month of the data, then save the transformed data into `silver`.

> _If the month is odd, you will only keep the long trips, otherwise you will keep the expensive ones_

🧐 Granted, this condition makes no real business sense, but it's an easy one, and we've given you the python logic in  `is_month_odd` already - let's move on and focus on Airflow logic!


**❓You need to code five tasks (code the tasks and DAG first, then code the python-functions)**

1. [`extract_sensor`](https://airflow.apache.org/docs/apache-airflow/stable/concepts/sensors.html) that should wait for the DAG `extract` to be in the `success` state, and check its state every 10 seconds for a maximum of 10 minutes (after that, it should timeout). No need to specify an external `task_id`, such that it will wait for the DAG itself to succeed

2. `is_month_odd` a [BranchPythonOperator](https://airflow.apache.org/docs/apache-airflow/1.10.6/concepts.html?highlight=branch+operator#branching) that should trigger the `is_month_odd` function with the proper arguments

3. `filter_long_trips` that should trigger the `filter_long_trips` function with the proper arguments (set the `distance` argument to `150`)

4. `filter_expensive_trips` that should trigger the `filter_expensive_trips` function with the proper arguments (set the `amount` argument to `500`)

5. a `EmptyOperator` with a `task_id` named `end`. As the fifth task should be triggered as soon as one of the third/fourth task is successful (only one of both will run), let's set its trigger_rule to [`one_success`](https://airflow.apache.org/docs/apache-airflow/1.10.5/concepts.html?highlight=trigger+rule#trigger-rules). If you wonder why we added an EmptyOperator at the end, this is just to have a single task closing your DAG and not two distinct branches which is more visual.

Ordering:
- The second task should be triggered only once the first one succeeds.
- The third or the fourth task should be triggered based on the return of the second one.
- The fifth task should be triggered only once the third/fourth one succeeds.


❓ **Try to run your DAG with python functions!**

🧪 Then test yourself
```bash
make test_transform_dag
```


# 3️⃣ "Load" DAG

<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/airflow_advanced_load_dag.png">

The main goal of this final DAG is to take the data you put in `silver` and to load it into `Google Cloud Storage` and then `BigQuery`.

## Setup GCP connections

We need to add a connection between Airflow and our GCP account, to be able to talk to GCS & Big Query.

🕵️‍♀️ **Time for you to do a bit of research**!
- Take 5 minute to read Airflow docs about [Managing Connections](https://airflow.apache.org/docs/apache-airflow/stable/howto/connection.html) and [Google Cloud Connection](https://airflow.apache.org/docs/apache-airflow-providers-google/stable/connections/gcp.html)
- Try to setup a connection using your GCP service account key that is stored somewhere on your VM
- We only ask you to name it "google_cloud_connection" so we can test it later on.

<details>
  <summary markdown='span'>🎁 Solution (don't look, try it before!)</summary>

You can do it directly from the Airflow UI: hover the `Admin` tab and select `Connections`. Click on the white cross to add a new record:
- name the `Connection Id` `google_cloud_connection`
- set the `Connection Type` to `Google Cloud`
- copy paste the whole content of your `service-account.json` to the `Keyfile JSON`

Or you can try the CLI by running

```bash
docker compose exec webserver poetry run airflow connections add "google_cloud_connection" \
--add-correct-arguments-here
```

</details>



## DAG
Once the bucket creation is done, let's move to your DAG.
You'll use the following airflow operator to ease your life:

```python
from airflow.providers.google.cloud.operators.bigquery import (
    BigQueryCreateEmptyDatasetOperator,
    BigQueryCreateEmptyTableOperator,
    BigQueryInsertJobOperator)
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import (
    LocalFilesystemToGCSOperator,
    GCSToBigQueryOperator)
```

This branch needs 6 tasks:
- `transform_sensor` that should wait for the DAG `transform` to be in the `success` state, and check its state every 10 seconds for a maximum of 10 minutes (after that it should timeout)
- `upload_local_file_to_gcs` that should load your local silver file to the Google Cloud Storage silver bucket with the same file's name. ❗️ You'll need to create a bucket on GCS first, hopefully that's a one liner:
  ```
  gsutil mb -l EU gs://de_airflow_taxi_silver
  ```
- `create_dataset` that should create the `de_airflow_taxi_gold` dataset on BigQuery
- `create_table` that should create a big-query table named `trips` in the dataset `de_airflow_taxi_gold` with the proper schema (`date` as a string and `trip_distance` & `total_amount` as floats)
- `remove_existing_data` that should run a query to remove data at the current date (in order to be idempotent)
- `load_to_bigquery` that should append the content of the `silver` file to the `gold` table

All tasks should be triggered in that order as soon as the previous one succeeded.

Once your confident with what you have done, run the following command:

```bash
make test_load_dag
```

WARNING: No to help you too much, we decided not to test everything in your tasks. This means that you need to manually launch the DAG and see if data is coming into your Google Cloud Storage & BigQuery instances and to update a bit your tasks if needed.

<details>
  <summary markdown='span'>💡 Hint</summary>
  You may need to set `useLegacySql` to False for the task_id `remove_existing_data`
  You may need to set `skip_leading_rows` & `write_disposition` for the task_id `load_to_bigquery`
</details>

# 🏁 Conclusion

This dummy ETL makes little business sense, but you are now equipped to use it for any real cases.

For instance, and related to this dataset, you could build the following graph:
(assume you already have a Machine-Learning model in production to predict taxi fares based on distances)

- Dag 1:
  - download new data every month on GCS
  - process new data into ML features and store on Big Query
- Dag 2:
  - wait for Dag 1
  - branch 1: evaluate ML model performance on new month's data
  - branch 2:
    - retrain ML model
    - then evaluate performance on new month's data
  - Compare the two models
  - Store best model's weights in GCS
- Dag 3:
  - Wait for Dag 2
  - Deploy best of two models in production


🧪 Store your results:
```
make test
git add --all
git commit -m "finalized challenge 030201"
git push origin main
```
