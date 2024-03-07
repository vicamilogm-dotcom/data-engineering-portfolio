import json
import os

from airflow.hooks.sqlite_hook import SqliteHook

from dags import local_etl
# Set this variable temporarily back to student-config but without affecting airflow test configuration.
os.environ["AIRFLOW_HOME"] = "/app/airflow"

def test_read_from_json():
    content = local_etl.read_from_json("tests/test_data/joke_without_single_quote.json")
    assert content == {
        "categories": [],
        "created_at": "2020-01-05 13:42:26.766831",
        "icon_url": "https://assets.chucknorris.host/img/avatar/chuck-norris.png",
        "id": "gldk0zH1Tqqa1-NHlHLn2A",
        "updated_at": "2020-01-05 13:42:26.766831",
        "url": "https://api.chucknorris.io/jokes/gldk0zH1Tqqa1-NHlHLn2A",
        "value": "Chuck Norris abducts aliens.",
    }
    content = local_etl.read_from_json("tests/test_data/joke_with_single_quote.json")
    assert content == {
        "categories": [],
        "created_at": "2020-01-05 13:42:26.766831",
        "icon_url": "https://assets.chucknorris.host/img/avatar/chuck-norris.png",
        "id": "gldk0zH1Tqqa1-NHlHLn2A",
        "updated_at": "2020-01-05 13:42:26.766831",
        "url": "https://api.chucknorris.io/jokes/gldk0zH1Tqqa1-NHlHLn2A",
        "value": "A diff between your code and Chuck Norris's is infinite.",
    }


def test_translate_joke_to_swedish():
    joke = local_etl.read_from_json("tests/test_data/joke_without_single_quote.json")["value"]
    translated_joke = local_etl.translate_joke_to_swedish(joke)
    assert translated_joke == "Chuck Norris bortf\u00f6r utl\u00e4nningar."
    joke = local_etl.read_from_json("tests/test_data/joke_with_single_quote.json")["value"]
    translated_joke = local_etl.translate_joke_to_swedish(joke)
    assert translated_joke == "En skillnad mellan din kod och Chuck Norris \u00e4r o\u00e4ndlig."


def test_write_jokes_to_json():
    joke = local_etl.read_from_json("tests/test_data/joke_without_single_quote.json")["value"]
    swedified_joke = local_etl.translate_joke_to_swedish(joke)
    temp_file = "tests/temp/swedified_joke.json"
    if os.path.isfile(temp_file):
        os.remove(temp_file)
    local_etl.write_jokes_to_json(temp_file, joke, swedified_joke)

    with open(temp_file, "r") as file:
        saved_joke = json.load(file)
        assert joke == saved_joke["joke"]
        assert swedified_joke == saved_joke["swedified_joke"]


def test_double_single_quote():
    joke = local_etl.read_from_json("tests/test_data/joke_with_single_quote.json")["value"]
    assert local_etl.double_single_quote(joke) == "A diff between your code and Chuck Norris''s is infinite."
    joke = local_etl.read_from_json("tests/test_data/joke_without_single_quote.json")["value"]
    assert local_etl.double_single_quote(joke) == joke


def test_transform():
    temp_file = "tests/temp/swedified_joke.json"
    if os.path.isfile(temp_file):
        os.remove(temp_file)
    local_etl.transform("tests/test_data/joke_with_single_quote.json", temp_file)

    with open(temp_file, "r") as file:
        joke = json.load(file)
        assert joke["joke"] == "A diff between your code and Chuck Norris''s is infinite."
        assert joke["swedified_joke"] == "En skillnad mellan din kod och Chuck Norris \u00e4r o\u00e4ndlig."


def test_load_to_database():
    hook = SqliteHook(sqlite_conn_id="sqlite_connection")
    hook.run(sql="DROP TABLE IF EXISTS swedified_jokes;")
    hook.run(
        sql="""CREATE TABLE swedified_jokes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                joke VARCHAR NOT NULL,
                swedified_joke VARCHAR NOT NULL
            );"""
    )

    assert hook.get_records("SELECT COUNT(*) FROM swedified_jokes;")[0][0] == 0
    local_etl.load("tests/test_data/swedified_joke.json", hook)
    assert hook.get_records("SELECT COUNT(*) FROM swedified_jokes;")[0][0] == 1
    joke = (
        "Chuck Norris doesnt use a microwave to pop his popcorn. He simply sits the package on the counter "
        "and the kernals jump in fear of a round house kick"
    )
    swedified_joke = (
        "Chuck Norris använder inte en mikrovågsugn för att poppa sin popcorn.Han sitter helt "
        "enkelt paketet på räknaren och kernalerna hoppar i rädsla för en rund husspark"
    )
    assert hook.get_records("SELECT * FROM swedified_jokes;")[0] == (1, joke, swedified_joke)
    local_etl.load("tests/test_data/swedified_joke.json", hook)
    assert hook.get_records("SELECT COUNT(*) FROM swedified_jokes;")[0][0] == 2
