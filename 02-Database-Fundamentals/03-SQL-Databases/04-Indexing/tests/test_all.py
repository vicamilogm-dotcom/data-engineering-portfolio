import pathlib
import os

import pandas as pd
from pandas.api import types as ptypes

import lewagonde

from lwdb.db import query_perf


def prep_db():
    parent_dir = pathlib.Path(os.path.realpath(__file__)).parent.parent
    dot_env_fp = os.path.join(parent_dir, ".env")
    lewagonde.load_dot_env(dot_env_fp)


def test_csv_raw():
    """
    Test that the generated CSV is present
    """
    parent_dir = pathlib.Path(os.path.realpath(__file__)).parent.parent
    pq_fp = os.path.join(parent_dir, "data", "ikea-cols.parquet")
    df = pd.read_parquet(pq_fp)
    columns = set(
        [
            "product_title",
            "product_url",
            "sku",
            "mpn",
            "currency",
            "product_price",
            "product_condition",
            "availability",
            "seller",
            "seller_url",
            "brand",
            "raw_product_details",
            "breadcrumbs",
            "country",
            "language",
            "average_rating",
            "reviews_count",
        ]
    )
    assert set(df.columns) == columns, f"Wrong columns in the CSV, expected {columns}"


def test_csv_cleaned():
    parent_dir = pathlib.Path(os.path.realpath(__file__)).parent.parent
    csv_fp = os.path.join(parent_dir, "data", "ikea-rows.csv")
    assert os.path.isfile(
        csv_fp
    ), f"File {csv_fp} not present, fill in `cast_columns` then call `save_df_to_csv`"
    df = pd.read_csv(csv_fp)
    assert (
        ptypes.is_numeric_dtype(df.product_price)
        and ptypes.is_numeric_dtype(df.average_rating)
        and ptypes.is_numeric_dtype(df.reviews_count)
    ), "product_price, average_rating must have numeric types and reviews_count be integer"


def test_table_creation():
    prep_db()
    df = lewagonde.read_sql_query(
        "SELECT * FROM ikea_products LIMIT 1;",
        password=os.environ["POSTGRES_PASSWORD"],
        user=os.environ.get("USER", ""),
        host="0.0.0.0",
        port="5432",
        dbname="ikea",
    )
    columns = set(
        [
            "product_title",
            "product_url",
            "sku",
            "mpn",
            "currency",
            "product_price",
            "product_condition",
            "availability",
            "seller",
            "seller_url",
            "brand",
            "raw_product_details",
            "breadcrumbs",
            "country",
            "language",
            "average_rating",
            "reviews_count",
        ]
    )
    assert columns <= set(df.columns), f"Wrong columns in the table, expected {columns}"


def test_data_loaded():
    """
    Test that the CSV was loaded in the DB with the right schema
    """
    df = lewagonde.read_sql_query(
        "SELECT COUNT(*) AS count FROM ikea_products;",
        password=os.environ["POSTGRES_PASSWORD"],
        user=os.environ.get("USER", ""),
        host="0.0.0.0",
        port="5432",
        dbname="ikea",
    )
    assert df["count"].iloc[0] > 10000, "Data doesn't seem to be loaded"


def test_search_chair():
    parent_dir = pathlib.Path(os.path.realpath(__file__)).parent.parent
    sql_file_path = os.path.join(parent_dir, "sql", "search-chair.sql")
    _, results = query_perf(sql_file_path=sql_file_path)
    assert results.iloc[0, 0] > 25, "we should find more than 25 results"


def test_btree_index():
    """
    Test that a BTree index on the SKU was added
    """
    _, results = query_perf(
        sql_query="select count(*) as count from pg_indexes where indexname = 'index_sku';"
    )
    assert (
        results.iloc[0]["count"] == 1
    ), "BTree index not added, make sure to name it 'index_sku'"


def test_add_text_col():
    """
    Test that column 'raw_product_details_text' exists in table 'ikea_products'
    """
    _, results = query_perf(
        sql_query="""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = 'ikea_products';
        """
    )
    assert (
        "raw_product_details_text" in results["column_name"].values
    ), "Column 'raw_product_details_text' does not exist in table 'ikea_products'"


def test_fulltext():
    """
    Test that a full text search index on the raw_product_details was added
    """
    _, results = query_perf(
        sql_query="select count(*) as count from pg_indexes where indexname = 'index_raw_product_details_text';"
    )
    assert (
        results.iloc[0]["count"] == 1
    ), "Full text index not found, name it 'index_raw_product_details_text'"


def test_search_chair_indexed():
    parent_dir = pathlib.Path(os.path.realpath(__file__)).parent.parent
    sql_file_path = os.path.join(parent_dir, "sql", "search-chair-indexed.sql")
    _, results = query_perf(sql_file_path=sql_file_path)
    assert (
        results.iloc[0, 0] > 25
    ), "search-chair-indexed.sql seems wrong, finding less than 25 values, expected more"
