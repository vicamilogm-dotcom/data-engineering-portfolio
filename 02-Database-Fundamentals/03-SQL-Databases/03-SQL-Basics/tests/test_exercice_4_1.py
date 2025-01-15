import os
import pathlib
import lewagonde

lewagonde.load_dot_env()
exercice_4_1_1 = pathlib.Path(os.path.dirname(__file__)).parent.joinpath(
    "exercice-4-1.sql"
)

with open(exercice_4_1_1, "r") as f:
    df_4_1_1 = lewagonde.read_sql_query(
        f.read(),
        password=os.environ.get("POSTGRES_PASSWORD", ""),
        user=os.environ.get("USER", ""),
        host="localhost",
        dbname="movies",
    )


def test_duplicate_movies_metadata():
    columns_set = set(df_4_1_1.columns)
    assert columns_set == set(
        ["id", "num_records"]
    ), "Column names of the output are incorrect"

    duplicate_example = df_4_1_1[df_4_1_1["id"] == 25541]
    assert (
        len(duplicate_example) == 1
    ), "Your output should include id = 25541, which is duplicated in the table"

    assert (
        len(df_4_1_1) == 29
    ), "There should be 29 duplicated IDs in the movies_metadata table"
