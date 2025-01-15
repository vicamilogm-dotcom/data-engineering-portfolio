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
        dbname="school",
    )
    loaded_tables = set(df_schemas["table_name"].tolist())
    assert (
        set(["teachers"]) <= loaded_tables
    ), "Tables 'teachers' not loaded, or incorrect table name"
    assert (
        set(["students"]) <= loaded_tables
    ), "Tables 'students' not loaded, or incorrect table name"
