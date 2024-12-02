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


def test_int_sales_margin_structure():
    output = client.query(sql_query_table_structure("int_sales_margin", bq_dataset))
    df = output.to_dataframe()
    expected_columns = set(
        [
            "products_id",
            "date_date",
            "orders_id",
            "revenue",
            "quantity",
            "purchase_price",
            "purchase_cost",
            "margin",
        ]
    )
    assert len(df) >= 1, "int_sales_margin model has not been created"
    if len(df) >= 1:
        actual_columns = set(df["column_name"].tolist())
        assert expected_columns.issubset(
            actual_columns
        ), "int_sales_margin model has missing columns"


def test_int_orders_margin_structure():
    output = client.query(sql_query_table_structure("int_orders_margin", bq_dataset))
    df = output.to_dataframe()
    expected_columns = set(
        [
            "orders_id",
            "date_date",
            "revenue",
            "quantity",
            "purchase_cost",
            "margin",
        ]
    )
    assert len(df) >= 1, "int_orders_margin model has not been created"
    if len(df) >= 1:
        actual_columns = set(df["column_name"].tolist())
        assert expected_columns.issubset(
            actual_columns
        ), "int_orders_margin model has missing columns"


def test_int_orders__structure():
    output = client.query(
        sql_query_table_structure("int_orders_operational", bq_dataset)
    )
    df = output.to_dataframe()
    expected_columns = set(
        [
            "orders_id",
            "date_date",
            "operational_margin",
            "quantity",
            "purchase_cost",
            "margin",
            "shipping_fee",
            "log_cost",
            "ship_cost",
        ]
    )
    assert len(df) >= 1, "int_orders_operational model has not been created"
    if len(df) >= 1:
        actual_columns = set(df["column_name"].tolist())
        assert expected_columns.issubset(
            actual_columns
        ), "int_orders_operational model has missing columns"
