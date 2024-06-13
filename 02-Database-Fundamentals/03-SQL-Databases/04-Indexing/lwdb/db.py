import os
import pandas as pd
import pathlib
import time
from typing import Tuple
import psycopg2 as pg
import lewagonde


def query_perf(
    sql_query: str = "", sql_file_path: str = ""
) -> Tuple[float, pd.DataFrame]:
    """
    Measure a query performance by passing EITHER a `sql_query` string of the `sql_file_path`.
    """
    assert len([q for q in [sql_query, sql_file_path] if q != ""]) == 1
    if sql_file_path != "":
        sql_query = open(sql_file_path).read()
    parent_dir = pathlib.Path(os.path.realpath(__file__)).parent.parent
    dot_env_fp = os.path.join(parent_dir, ".env")
    lewagonde.load_dot_env(dot_env_fp)

    con = pg.connect(database="ikea")

    try:
        t0 = time.time()
        result_df = pd.read_sql_query(
            sql=sql_query,
            con=con,
        )
        dt_seconds = time.time() - t0
        return dt_seconds, result_df
    except BaseException as e:
        raise e
    finally:
        con.close()
