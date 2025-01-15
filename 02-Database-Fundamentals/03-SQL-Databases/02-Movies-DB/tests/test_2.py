import os

import lewagonde


lewagonde.load_dot_env()


def test_correct_tables():
    lewagonde.load_dot_env()
    df_schemas = lewagonde.read_sql_query(
        "SELECT * \
        FROM INFORMATION_SCHEMA.TABLES \
        WHERE table_schema = 'public'",
        password=os.environ.get("POSTGRES_PASSWORD", ""),
        user=os.environ.get("USER", ""),
        host="localhost",
        dbname="movies",
    )
    loaded_tables = set(df_schemas["table_name"].tolist())
    assert (
        set(["ratings"]) <= loaded_tables
    ), "Tables 'ratings' not loaded, or incorrect table name"


def test_correct_column_names_and_types():
    df_columns = lewagonde.read_sql_query(
        "SELECT * \
        FROM INFORMATION_SCHEMA.COLUMNS \
        WHERE table_name = 'ratings' \
        ",
        password=os.environ.get("POSTGRES_PASSWORD", ""),
        user=os.environ.get("USER", ""),
        host="localhost",
        dbname="movies",
    )

    timestamp_column = df_columns[
        (df_columns["table_name"] == "ratings")
        & (df_columns["column_name"] == "timestamp")
    ]

    assert (
        len(timestamp_column) == 1
    ), "timestamp column in ratings table not loaded - or incorrectly spelled"
    assert set(df_columns["column_name"]) == set(
        ["user_id", "movie_id", "rating", "timestamp", "created_at_utc"]
    ), "list of columns in ratings table is incorrect, or incorrectly spelled"
