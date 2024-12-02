import os
import pathlib

# current_file = '/Users/nicolasbancel/git/lewagon/data-engineering-solutions/02-Data-at-Scales/01-ELT-DBT/04-DBT-Optimization-Optional/tests/test_sql_macros.py'
# challenge_level_dir =  pathlib.Path(os.path.realpath(current_file)).parent.parent


challenge_level_dir = pathlib.Path(os.path.realpath(__file__)).parent.parent
mart_user_macro_path = pathlib.Path(
    os.path.join(challenge_level_dir, "dbt_lewagon/macros/models/mart_user.sql")
)


def test_mart_user_macro_file_created():
    assert (
        mart_user_macro_path.is_file()
    ), "macros/models/mart_user.sql has not been created"
