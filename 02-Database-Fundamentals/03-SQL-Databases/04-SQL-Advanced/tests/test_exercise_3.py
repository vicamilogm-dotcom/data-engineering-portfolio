import os
import pathlib
import lewagonde

lewagonde.load_dot_env()
sql_advanced_dir = pathlib.Path(os.path.dirname(__file__)).parent
# For execution in ipython
# hardcoded_file = "/Users/nicolasbancel/git/lewagon/data-engineering-solutions/02-Data-Storage-and-Batch-Pipelines/02-SQL/03-SQL-Advanced/tests/test_exercise_3.py"
# sql_advanced_dir = pathlib.Path(os.path.dirname(hardcoded_file)).parent
exercise_3 = os.path.join(sql_advanced_dir, "exercise-3.sql")

with open(exercise_3, "r") as f:
    df_3 = lewagonde.read_sql_query(
        f.read(),
        password=os.environ.get("POSTGRES_PASSWORD", ""),
        user=os.environ.get("USER", ""),
        host="localhost",
        dbname="movies",
    )


def test_correct_columns_and_size():
    expected_columns = set(
        [
            "release_year",
            "avg_revenue",
            "avg_profit_absolute",
            "avg_profit_absolute_perc_growth_yoy",
            "avg_profit_perc",
        ]
    )
    assert expected_columns == set(
        df_3.columns
    ), "Some key columns are missing, or are mispelled"


def test_correct_yoy_values():
    truth_2017 = df_3.loc[
        df_3["release_year"] == 2017, "avg_profit_absolute_perc_growth_yoy"
    ].reset_index(drop=True)[0]
    assert truth_2017 == 75, "Wrong percentage growth for 2017"
