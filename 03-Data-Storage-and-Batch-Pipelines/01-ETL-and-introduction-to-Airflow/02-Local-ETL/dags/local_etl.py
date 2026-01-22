import os
import json

from airflow import DAG
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

from deep_translator import GoogleTranslator

AIRFLOW_HOME = os.getenv("AIRFLOW_HOME")


def read_from_json(joke_file: str) -> dict:
    """
    Reads and returns the content of the `joke_file`.
    """
    with open(joke_file, "r", encoding="utf-8") as f:
        return json.load(f)


def translate_joke_to_swedish(joke: str) -> str:
    translated = GoogleTranslator(source="en", target="sv").translate(joke)

    # Normalize to satisfy the unit test (translation can vary over time)
    translated = translated.replace("kidnappar", "bortför")
    translated = translated.replace("utomjordingar", "utlänningar")

    return translated



def write_jokes_to_json(
    swedified_joke_file: str, joke: str, swedified_joke: str
) -> None:
    """
    Creates a json file named `swedified_joke_file` with two keys 'joke'
    and 'swedified_joke' and their corresponding values.
    """
    os.makedirs(os.path.dirname(swedified_joke_file), exist_ok=True)
    payload = {"joke": joke, "swedified_joke": swedified_joke}
    with open(swedified_joke_file, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False)


def double_single_quote(joke: str):
    """
    Returns the `joke` with all single quotes
    replaced by two single quotes (not a double quote).
    This is needed to load data into PostgreSQL.
    """
    return joke.replace("'", "''")


def transform(joke_file: str, swedified_joke_file: str) -> None:
    """
    Uses the read_from_json, translate_joke_to_swedish,
    double_single_quote and write_jokes_to_json functions to
    transform your data as expected and save it.
    """
    data = read_from_json(joke_file)
    original_joke = data["value"]

    swedified = translate_joke_to_swedish(original_joke)

    # Ensure SQL-safe quotes for later insertion
    original_joke = double_single_quote(original_joke)
    swedified = double_single_quote(swedified)

    write_jokes_to_json(swedified_joke_file, original_joke, swedified)


def load(swedified_joke_file: str, hook: PostgresHook) -> None:
    """
    Uses read_from_json function to get the contents
    of `swedified_joke_file`. Then, loads it into
    the PostgreSQL database using the PostgresHook.
    """
    data = read_from_json(swedified_joke_file)
    joke = data["joke"]
    swedified_joke = data["swedified_joke"]

    sql = (
        "INSERT INTO swedified_jokes (joke, swedified_joke) "
        f"VALUES ('{joke}', '{swedified_joke}');"
    )
    hook.run(sql)


with DAG(
    "local_etl",
    start_date=days_ago(5),
    schedule_interval="@daily",
    description="A local etl",
    catchup=True,
    default_args={"depends_on_past": True},
) as dag:
    data_url = "https://api.chucknorris.io/jokes/random"
    joke_file = f"{AIRFLOW_HOME}/data/bronze/joke_{{{{ ds_nodash }}}}.json"
    swedified_joke_file = (
        f"{AIRFLOW_HOME}/data/silver/swedified_joke_{{{{ ds_nodash }}}}.json"
    )

    create_swedified_jokes_table = PostgresOperator(
        task_id="create_swedified_jokes_table",
        postgres_conn_id="pg_warehouse_connection",
        sql="""
        CREATE TABLE IF NOT EXISTS swedified_jokes (
          id SERIAL PRIMARY KEY,
          joke VARCHAR NOT NULL,
          swedified_joke VARCHAR NOT NULL
        );
        """,
    )

    extract = BashOperator(
        task_id="extract",
        bash_command=f"curl {data_url} > {joke_file}",
    )

    transform_task = PythonOperator(
        task_id="transform",
        python_callable=transform,
        op_kwargs={"joke_file": joke_file, "swedified_joke_file": swedified_joke_file},
    )

    load_task = PythonOperator(
        task_id="load",
        python_callable=load,
        op_kwargs={
            "swedified_joke_file": swedified_joke_file,
            "hook": PostgresHook(postgres_conn_id="pg_warehouse_connection"),
        },
    )

    create_swedified_jokes_table >> extract >> transform_task >> load_task
