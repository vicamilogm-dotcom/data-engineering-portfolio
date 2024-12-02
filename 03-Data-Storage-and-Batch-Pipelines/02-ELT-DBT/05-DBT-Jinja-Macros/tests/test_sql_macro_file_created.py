import pathlib


challenge_level_dir = pathlib.Path(__file__).parent.parent
mart_user_macro_path = (
    challenge_level_dir / "dbt_lewagon/macros/functions.sql"
).resolve()


def test_mart_user_macro_file_created():
    assert mart_user_macro_path.is_file(), "macros/functions.sql has not been created"
