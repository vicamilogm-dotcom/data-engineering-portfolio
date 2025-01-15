import os

import lewagonde


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
        set(["movies_metadata"]) <= loaded_tables
    ), "Tables 'movies_metadata' not loaded, or incorrect table name"


def test_correct_column_name_and_types():
    df_columns = lewagonde.read_sql_query(
        "SELECT * \
        FROM INFORMATION_SCHEMA.COLUMNS \
        WHERE table_name = 'movies_metadata' \
        ",
        password=os.environ.get("POSTGRES_PASSWORD", ""),
        user=os.environ.get("USER", ""),
        host="localhost",
        dbname="movies",
    )
    video_column = df_columns[
        (df_columns["table_name"] == "movies_metadata")
        & (df_columns["column_name"] == "video")
    ]
    adult_column = df_columns[
        (df_columns["table_name"] == "movies_metadata")
        & (df_columns["column_name"] == "adult")
    ]

    assert (
        len(adult_column) == 1
    ), "adult column in movies_metadata table not loaded - or incorrectly spelled"
    assert (
        len(video_column) == 1
    ), "video column in movies_metadata table not loaded - or incorrectly spelled"
    assert (
        len(adult_column[adult_column["data_type"] == "boolean"]) == 1
    ), "adult column in movies_metadata table has not been converted to correct data type"
    assert (
        len(video_column[video_column["data_type"] == "boolean"]) == 1
    ), "video column in movies_metadata table has not been converted to correct data type"
