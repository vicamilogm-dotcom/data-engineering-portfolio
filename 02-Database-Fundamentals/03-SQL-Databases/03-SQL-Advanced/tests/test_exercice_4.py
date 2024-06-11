import os
import pathlib
import lewagonde

lewagonde.load_dot_env()
sql_advanced_dir = pathlib.Path(os.path.dirname(__file__)).parent
# For execution in ipython
# hardcoded_file = "/Users/nicolasbancel/git/lewagon/data-engineering-solutions/02-Data-Storage-and-Batch-Pipelines/02-SQL/03-SQL-Advanced/tests/test_exercice_4.py"
# sql_advanced_dir = pathlib.Path(os.path.dirname(hardcoded_file)).parent
exercice_4 = os.path.join(sql_advanced_dir, "exercice-4.sql")

with open(exercice_4, "r") as f:
    df_4 = lewagonde.read_sql_query(
        f.read(),
        password=os.environ.get("POSTGRES_PASSWORD", ""),
        user=os.environ.get("USER", ""),
        host="localhost",
        dbname="movies",
    )


def test_correct_columns_and_size():
    expected_columns = set(["num_records_bad", "num_records_total", "perc_records_bad"])
    assert expected_columns == set(
        df_4.columns
    ), "Some key columns are missing, or are mispelled"


def test_correct_metric_calculation():
    num_records_bad_expected = 40082
    num_records_total_expected = 45463
    perc_records_bad_expected = 88

    num_records_bad = df_4["num_records_bad"][0]
    num_records_total = df_4["num_records_total"][0]
    perc_records_bad = df_4["perc_records_bad"][0]

    assert (
        num_records_bad_expected == num_records_bad
    ), "There should be 40082 bad records"
    assert (
        num_records_total_expected == num_records_total
    ), "There should be 45463 total records"
    assert (
        perc_records_bad_expected == perc_records_bad
    ), "There should be 88% of all records that are 'bad'"
