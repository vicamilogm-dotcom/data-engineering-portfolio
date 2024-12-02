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


def test_mart_user_structure_first_exercice():
    output = client.query(sql_query_table_structure("mart_user", bq_dataset))
    df = output.to_dataframe()
    expected_columns = set(
        [
            "user_id",
            "num_comments",
            "first_comment_at",
            "last_comment_at",
            "num_stories",
            "first_story_at",
            "last_story_at",
        ]
    )
    assert len(df) >= 1, "mart_user model has not been created"
    if len(df) >= 1:
        actual_columns = set(df["column_name"].tolist())
        assert expected_columns.issubset(
            actual_columns
        ), "mart_user model has missing columns"


def test_mart_user_structure_second_exercice():
    """
    Second part of the exercice is to add the `user_url` column
    To facilitate the QA
    """
    output = client.query(sql_query_table_structure("mart_user", bq_dataset))
    df = output.to_dataframe()
    if len(df) >= 1:
        actual_columns = set(df["column_name"].tolist())
        assert (
            "user_url" in actual_columns
        ), "mart_user model user_url field has not been added"
