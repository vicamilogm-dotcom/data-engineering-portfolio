import os
import pathlib

# current_file = '/Users/nicolasbancel/git/lewagon/data-engineering-solutions/02-Data-at-Scales/01-ELT-DBT/04-DBT-Optimization-Optional/tests/test_sql_macros.py'
# challenge_level_dir =  pathlib.Path(os.path.realpath(current_file)).parent.parent


challenge_level_dir = pathlib.Path(os.path.realpath(__file__)).parent.parent
mart_user_macro_path = pathlib.Path(
    os.path.join(challenge_level_dir, "dbt_lewagon/macros/models/mart_user.sql")
)
mart_user_model_path = pathlib.Path(
    os.path.join(challenge_level_dir, "dbt_lewagon/models/mart/mart_user.sql")
)

with open(mart_user_macro_path) as f:
    mart_user_macro_sql = f.read()

with open(mart_user_model_path) as file:
    mart_user_model_sql = file.read()

num_types_macro = "num_types(type)"
first_type_at_macro = "first_type_at(type)"
last_type_at_macro = "last_type_at(type)"
key_metrics_per_type_macro = "key_metrics_per_type(type)"

key_metrics_per_type_usage = "{{ key_metrics_per_type("


def test_first_3_mart_user_macros_created():
    assert (
        num_types_macro in mart_user_macro_sql
    ), "num_types macro has not been created"
    assert (
        first_type_at_macro in mart_user_macro_sql
    ), "first_type_at macro has not been created"
    assert (
        last_type_at_macro in mart_user_macro_sql
    ), "last_type_at macro has not been created"


def test_last_mart_user_macro_created():
    assert (
        key_metrics_per_type_macro in mart_user_macro_sql
    ), "key_metrics_per_type macro has not been created"


def test_last_mart_user_macro_used():
    assert key_metrics_per_type_usage.replace(" ", "") in mart_user_model_sql.replace(
        " ", ""
    ), "key_metrics_per_type macro is not used in mart_user model"
