import os
import pathlib

# current_file = '/Users/nicolasbancel/git/lewagon/data-engineering-solutions/02-Data-at-Scales/01-ELT-DBT/04-DBT-Optimization-Optional/tests/test_dbt_variable.py'
# challenge_level_dir =  pathlib.Path(os.path.realpath(current_file)).parent.parent


challenge_level_dir = pathlib.Path(os.path.realpath(__file__)).parent.parent
dbt_project_path = pathlib.Path(
    os.path.join(challenge_level_dir, "dbt_lewagon/dbt_project.yml")
)


def test_dbt_project_created():
    assert dbt_project_path.is_file(), "dbt_project.yml has not been created"
