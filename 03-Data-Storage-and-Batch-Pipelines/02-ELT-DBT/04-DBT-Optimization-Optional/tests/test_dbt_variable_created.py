import os
import pathlib
import yaml

# current_file = '/Users/nicolasbancel/git/lewagon/data-engineering-solutions/02-Data-at-Scales/01-ELT-DBT/04-DBT-Optimization-Optional/tests/test_dbt_variable.py'
# challenge_level_dir =  pathlib.Path(os.path.realpath(current_file)).parent.parent


challenge_level_dir = pathlib.Path(os.path.realpath(__file__)).parent.parent
dbt_project_path = pathlib.Path(
    os.path.join(challenge_level_dir, "dbt_lewagon/dbt_project.yml")
)

with open(dbt_project_path) as f:
    dbt_project_yml = yaml.safe_load(f)


def test_vars_created():
    assert (
        dbt_project_yml.get("vars") is not None
    ), "variables not set in dbt_project.yml"


def test_vars_correct_setup():
    assert (
        dbt_project_yml.get("vars").get("last_x_days_history") is not None
    ), "Variable name is incorrect"
    assert (
        dbt_project_yml.get("vars").get("last_x_days_history") == 1000
    ), "Variable value is incorrect"
