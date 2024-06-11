import os
import pathlib
import lewagonde

lewagonde.load_dot_env()
sql_basics_dir = pathlib.Path(os.path.dirname(__file__)).parent

exercice_5 = os.path.join(sql_basics_dir, "exercice-5.sql")

with open(exercice_5, "r") as f:
    df_5 = lewagonde.read_sql_query(
        f.read(),
        password=os.environ.get("POSTGRES_PASSWORD", ""),
        user=os.environ.get("USER", ""),
        host="localhost",
        dbname="movies",
    )


def test_referential_integrity():
    columns_set = set(df_5.columns)
    assert columns_set == set(
        ["movie_id_ratings_table"]
    ), "Column name of the output is incorrect"

    problematic_record_example_1 = df_5[df_5["movie_id_ratings_table"] == 1014]
    assert (
        len(problematic_record_example_1) == 1
    ), "movie_id = 1014 is a problematic record - it should appear in your result, only 1 time"

    problematic_record_example_2 = df_5[df_5["movie_id_ratings_table"] == 112064]
    assert (
        len(problematic_record_example_2) == 1
    ), "movie_id = 112064 is a problematic record - it should appear in your result, only 1 time"

    assert (
        len(df_5) == 37550
    ), "There should be a total of 37550 records that are failing (37550 movie_ids in ratings that don't exist in movies_metadata"
