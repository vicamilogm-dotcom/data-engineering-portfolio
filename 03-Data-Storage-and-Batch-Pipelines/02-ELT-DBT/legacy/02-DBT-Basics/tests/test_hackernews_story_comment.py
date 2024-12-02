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


def test_hackernews_story_structure():
    output = client.query(sql_query_table_structure("stg_hackernews_story", bq_dataset))
    df = output.to_dataframe()
    expected_columns = set(
        [
            "story_id",
            "title",
            "author",
            "created_at_local",
            "text",
            "original_url",
            "is_deleted",
            "is_dead",
            "ranking",
            "row_created_at_local",
        ]
    )
    assert len(df) >= 1, "stg_hackernews_story model has not been created"
    if len(df) >= 1:
        actual_columns = set(df["column_name"].tolist())
        assert (
            expected_columns == actual_columns
        ), "stg_hackernews_story model columns are incorrect"


def test_hackernews_comment_structure():
    output = client.query(
        sql_query_table_structure("stg_hackernews_comment", bq_dataset)
    )
    df = output.to_dataframe()
    expected_columns = set(
        [
            "comment_id",
            "comment_parent_id",
            "author",
            "created_at_local",
            "text",
            "original_url",
            "is_deleted",
            "is_dead",
            "ranking",
            "row_created_at_local",
        ]
    )
    assert len(df) >= 1, "stg_hackernews_comment model has not been created"
    if len(df) >= 1:
        actual_columns = set(df["column_name"].tolist())
        assert (
            expected_columns == actual_columns
        ), "stg_hackernews_comment model columns are incorrect"
