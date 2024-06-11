import os

from airflow import DAG
from airflow.providers.postgres.hooks.postgres import PostgresHook

# IMPORT YOUR PACKAGES HERE

AIRFLOW_HOME = os.getenv("AIRFLOW_HOME")


def read_from_json(joke_file: str) -> dict:
    """
    Reads and returns the content of the `joke_file`.
    """
    pass  # YOUR CODE HERE


def translate_joke_to_swedish(joke: str) -> str:
    """
    Returns the translated to Swedish joke using
    the googletrans library: https://github.com/ssut/py-googletrans
    """
    pass  # YOUR CODE HERE


def write_jokes_to_json(
    swedified_joke_file: str, joke: str, swedified_joke: str
) -> None:
    """
    Creates a json file named `swedified_joke_file` with two keys 'joke'
    and 'swedified_joke' and their corresponding values.
    """
    pass  # YOUR CODE HERE


def double_single_quote(joke: str):
    """
    Returns the `joke` with all single quotes
    replaced by two single quotes (not a double quote).
    This is needed to load data into PostgreSQL.
    """
    pass  # YOUR CODE HERE


def transform(joke_file: str, swedified_joke_file: str) -> None:
    """
    Uses the read_from_json, translate_joke_to_swedish,
    double_single_quote and write_jokes_to_json functions to
    transform your data as expected and save it.
    """
    pass  # YOUR CODE HERE


def load(swedified_joke_file: str, hook: PostgresHook) -> None:
    """
    Uses read_from_json function to get the contents
    of `swedified_joke_file`. Then, loads it into
    the PostgreSQL database using the PostgresHook.
    It is not idempotent as it will insert the same comments if we
    trigger the same task twice, but this is what we want.

    Warnings:
    As for the tests we use a sqlite database while you use a postgresql one
    in your docker, there are two things to take into account to solve this
    challenge and have green tests:

    1) Do not call the insert_rows function on your hook. It would make your DAG run
    but the tests will fail. You should instead call the run function on your hook.
    (The insert_rows and run functions are coming from the PostgresHook class which is
    why you don't see them in the current file.)

    2) Be careful to put single quotes around your inserted values. The first tests could pass
    but you would be blocked at the last one and your DAG would not run.
    Indeed, in postgresql the following syntax would raise an error (while it would be accepted in sqlite):
        INSERT INTO table (column) VALUES ("example")
    It should be:
        INSERT INTO table (column) VALUES ('example')
    """
    pass  # YOUR CODE HERE


with DAG(
    "local_etl",
    # YOUR CODE HERE
) as dag:
    data_url = "https://api.chucknorris.io/jokes/random"
    joke_file = f"{AIRFLOW_HOME}/data/bronze/joke_{{{{ ds_nodash }}}}.json"
    swedified_joke_file = (
        f"{AIRFLOW_HOME}/data/silver/swedified_joke_{{{{ ds_nodash }}}}.json"
    )

    pass  # YOUR CODE HERE
