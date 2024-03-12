import pytest
import psycopg2
import os
import pathlib
from decimal import Decimal

challenge_path = pathlib.Path(__file__).parent.parent.absolute()

DATABASE_CONFIG = {
    "dbname": "pagila",
    "user": os.environ["POSTGRES_USER"],
    "password": os.environ["POSTGRES_PASSWORD"],
    "host": "0.0.0.0",
    "port": "5410",
}


@pytest.fixture
def db_connection():
    conn = psycopg2.connect(**DATABASE_CONFIG)
    yield conn
    conn.close()


def read_sql(filename):
    with open(filename, "r") as file:
        return file.read()


def test_rental_duration_query(db_connection):
    sql = read_sql(challenge_path / "rental_duration_query.sql")
    cursor = db_connection.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    cursor.close()
    assert results[0] == ("KENNETH", "GOODEN", Decimal('6.59262152777777777708'), 4)
    assert results[-1] == ('TERRANCE', 'ROUSH', Decimal('5.01912202380952380714'), 2)


def test_co_stars_query(db_connection):
    sql = read_sql(challenge_path / "co_stars_query.sql")
    cursor = db_connection.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    cursor.close()
    assert results[0] == ("JULIA MCQUEEN", "HENRY BERRY", 7)
    assert results[-1] == ("ZERO CAGE", "SEAN WILLIAMS", 4)


def test_weekly_trends_query(db_connection):
    sql = read_sql(challenge_path / "weekly_trends_query.sql")
    cursor = db_connection.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    cursor.close()
    assert (
        str(results[0])
        == "(datetime.datetime(2022, 2, 14, 0, 0, tzinfo=datetime.timezone.utc), 182, Decimal('182.0000000000000000'), None, Decimal('0E-16'))"
    )
    assert (
        str(results[4])
        == "(datetime.datetime(2022, 6, 20, 0, 0, tzinfo=datetime.timezone.utc), 594, Decimal('874.6666666666666667'), -1123, Decimal('-280.6666666666666667'))"
    )


def test_last_rental_query(db_connection):
    sql = read_sql(challenge_path / "last_rental_query.sql")
    cursor = db_connection.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    cursor.close()
    assert (
        str(results[0])
        == "('HERBERT KRUGER', datetime.datetime(2022, 8, 16, 23, 40, 3, tzinfo=datetime.timezone.utc), 'Inactive')"
    )


def test_category_performance_query(db_connection):
    sql = read_sql(challenge_path / "category_performance_query.sql")
    cursor = db_connection.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    cursor.close()
    assert str(results[0]) == "('Foreign', Decimal('10507.67'), 'High')"
