import pytest
import psycopg2
import os
import pathlib

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


def test_actor_query(db_connection):
    sql = read_sql(challenge_path / "actor_query.sql")
    cursor = db_connection.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    cursor.close()
    assert results[:2] == [(107, 42), (102, 41)]


def test_rentals(db_connection):
    sql = read_sql(challenge_path / "rentals_query.sql")
    cursor = db_connection.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    cursor.close()
    assert results[:2] == [
        ("BUCKET BROTHERHOOD", "Music", 34),
        ("BUCKET BROTHERHOOD", "Games", 34),
    ]


def test_montly_revenue(db_connection):
    sql = read_sql(challenge_path / "monthly_revenue_query.sql")
    cursor = db_connection.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    cursor.close()
    results = results[:2]
    results = [(float(result[0]), float(result[1])) for result in results]
    assert results == [(1, 3094.78), (2, 10164.97)]
