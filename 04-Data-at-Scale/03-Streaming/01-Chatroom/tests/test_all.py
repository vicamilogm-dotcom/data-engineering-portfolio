import json
import os
import pathlib

import lewagonde


def get_tests_json():
    parent_dir = pathlib.Path(os.path.realpath(__file__)).parent.parent
    tests_json_fp = os.path.join(parent_dir, "tests.json")
    with open(tests_json_fp) as f:
        return json.load(f)


def test_docker_compose():
    parent_dir = pathlib.Path(os.path.realpath(__file__)).parent.parent
    dc_path = os.path.join(parent_dir, "docker-compose.yml")

    parent_dir = pathlib.Path(os.path.realpath(__file__)).parent
    dc_correction_path = os.path.join(parent_dir, "_x", "docker-compose.correction.yml")

    assert lewagonde.docker_compose_equal(
        dc_path, dc_correction_path, strict=False
    ), "Incorrect Docker Compose"


def test_exchange():
    assert (
        get_tests_json()["chat"] == "http://localhost:15672/#/exchanges/%2F/chat"
    ), "tests.json is incomplete, fill in the 'chat' value"


def test_simple_callback(capsys):
    from lwqueue.rabbitmq_subscriber import print_callback

    print_callback(None, None, None, "hello")
    captured_stdout = capsys.readouterr().out
    assert (
        "Received" in captured_stdout and "hello" in captured_stdout
    ), "print_callback should print 'Received' + the body"


def test_rich():
    from lwqueue.ui import make_rich_table

    table = make_rich_table(
        [{"message": "abcd", "received_at": "ok", "username": "john"}] * 2
    )
    assert table.row_count == 2


def test_queue():
    assert (
        get_tests_json()["queues"] == "http://localhost:15672/#/queues"
    ), "tests.json is incomplete, fill in the 'queues' value"
