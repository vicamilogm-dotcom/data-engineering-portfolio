import os
import pathlib
import lewagonde

lewagonde.load_dot_env()
sql_advanced_dir = pathlib.Path(os.path.dirname(__file__)).parent
exercice_1_1 = os.path.join(sql_advanced_dir, "exercice-1.sql")

with open(exercice_1_1, "r") as f:
    df_1_1 = lewagonde.read_sql_query(
        f.read(),
        password=os.environ.get("POSTGRES_PASSWORD", ""),
        user=os.environ.get("USER", ""),
        host="localhost",
        dbname="movies",
    )


def test_correct_columns():
    assert set(["id", "profit_absolute", "profit_percentage"]) <= set(
        df_1_1.columns
    ), "Some key columns are missing, or are mispelled"


def test_correct_filters():
    assert (
        df_1_1.loc[1, "id"] == 2667
    ), "Your filtering is incorrect - the #2 most profitable movie should be the id:2667 (The Blair Witch Project)"
    assert (
        len(df_1_1) == 5277
    ), "Your filtering is incorrect - the output should display 5277 records"
