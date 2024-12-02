import os
import yaml
import lewagonde
from google.cloud import bigquery
from google.oauth2 import service_account

dbt_profile_path = lewagonde.DBT_PROFILE_PATH
dbt_full_profile_path = os.path.expanduser(dbt_profile_path)

with open(dbt_full_profile_path) as f:
    profile_dict = yaml.safe_load(f)

dev = profile_dict["dbt_lewagon"]["outputs"]["dev"]
bq_dataset = dev["dataset"]
bq_project = dev["project"]
bq_credentials_path = dev["keyfile"]

credentials = service_account.Credentials.from_service_account_file(
    bq_credentials_path,
    scopes=["https://www.googleapis.com/auth/cloud-platform"],
)
client = bigquery.Client(credentials=credentials, project=credentials.project_id)


def sql_query_table_structure(model, bq_dataset):
    query = f"SELECT column_name \
    FROM `{bq_dataset}`.`INFORMATION_SCHEMA`.`COLUMNS` \
    WHERE table_name = '{model}'"
    return query


def test_stg_raw_sales_structure():
    output = client.query(sql_query_table_structure("stg_raw_sales", bq_dataset))
    df = output.to_dataframe()
    expected_columns = set(
        [
            "date_date",
            "orders_id",
            "products_id",
            "revenue",
            "quantity",
        ]
    )
    assert len(df) >= 1, "stg_raw_sales model has not been created"
    if len(df) >= 1:
        actual_columns = set(df["column_name"].tolist())
        assert (
            expected_columns == actual_columns
        ), "stg_raw_sales model columns are incorrect"


## TODO: add date constraint to dataset
# def test_stg_raw_sales_content():
#     sql_script = f"SELECT COUNT(DISTINCT(DATE(created_at_local))) AS num_days \
#     FROM `{bq_dataset}`.`stg_raw_sales` \
#     "
#     output = client.query(sql_script)
#     df = output.to_dataframe()

#     if len(df) >= 1:
#         assert (
#             df["num_days"][0] <= 1000
#         ), "You loaded more than 1000 days of data in stg_raw_sales"
