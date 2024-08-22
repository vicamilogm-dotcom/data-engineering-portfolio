import os
import pathlib
import yaml

challenge_level_dir = pathlib.Path(os.path.realpath(__file__)).parent.parent
dbt_lewagon_dir = os.path.join(challenge_level_dir, "dbt_lewagon/")

# Simplifying the structure of the root directories which are extremely long
# Transforming:
#  /home/selim/nico/data-engineering-solutions-week2/02-Data-at-Scales/01-ELT-DBT/dbt_lewagon/models'
# into
# dbt_lewagon/models


mart_models_path = os.path.join(dbt_lewagon_dir, "models/mart/models.yml")

with open(mart_models_path) as f:
    mart_models_yml = yaml.safe_load(f)


def test_documentation_file_populated_models():
    assert (
        mart_models_yml.get("models") is not None
    ), "models.yml should start with a models key"


def test_documentation_file_mart_user_populated():
    mart_user_doc = [
        value for value in mart_models_yml["models"] if value.get("name") == "mart_user"
    ]
    assert len(mart_user_doc) >= 1, "model mart_user not documented in models.yml"
    if len(mart_user_doc) >= 1:
        column_set = set([x["name"] for x in mart_user_doc[0]["columns"]])
        expected_column_set = set(
            [
                "user_id",
                "user_url",
                "num_comments",
                "first_comment_at",
                "last_comment_at",
                "num_stories",
                "first_story_at",
                "last_story_at",
            ]
        )
        assert (
            column_set == expected_column_set
        ), "Not all columns of mart_user are documented"


def test_documentation_file_mart_user_user_id_tested():
    mart_user_columns_doc = [
        value for value in mart_models_yml["models"] if value.get("name") == "mart_user"
    ][0]["columns"]
    num_tests_per_column = {}
    for column in mart_user_columns_doc:
        num_tests_per_column[column["name"]] = (
            0 if column.get("tests") is None else len(column.get("tests"))
        )
    assert (
        num_tests_per_column["user_id"] == 2
    ), "You did not implement 2 tests for the user_id column"


def test_documentation_file_mart_user_num_comments_tested():
    mart_user_columns_doc = [
        value for value in mart_models_yml["models"] if value.get("name") == "mart_user"
    ][0]["columns"]
    num_tests_per_column = {}
    for column in mart_user_columns_doc:
        num_tests_per_column[column["name"]] = (
            0 if column.get("tests") is None else len(column.get("tests"))
        )
    assert (
        num_tests_per_column["num_comments"] == 1
    ), "You did not implement 1 test for the num_comments column"


def test_documentation_file_mart_user_num_stories_tested():
    mart_user_columns_doc = [
        value for value in mart_models_yml["models"] if value.get("name") == "mart_user"
    ][0]["columns"]
    num_tests_per_column = {}
    for column in mart_user_columns_doc:
        num_tests_per_column[column["name"]] = (
            0 if column.get("tests") is None else len(column.get("tests"))
        )
    assert (
        num_tests_per_column["num_stories"] == 1
    ), "You did not implement 1 test for the num_comments column"
