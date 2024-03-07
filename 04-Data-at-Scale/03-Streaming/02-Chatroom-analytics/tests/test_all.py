import os
import pathlib
import lwqueue.clickhouse_queries as student_queries
from clickhouse_driver import Client
import lewagonde
import base64


def test_docker_compose():
    parent_dir = pathlib.Path(os.path.realpath(__file__)).parent.parent
    dc_path = os.path.join(parent_dir, "docker-compose.yml")

    parent_dir = pathlib.Path(os.path.realpath(__file__)).parent
    dc_correction_path = os.path.join(parent_dir, "_x", "docker-compose.correction.yml")

    assert lewagonde.docker_compose_equal(
        dc_path, dc_correction_path, strict=False
    ), "Incorrect Docker Compose"


def query_clickhouse(query):
    with Client(
        host="localhost",
        port=9000,
        user="rmq",
        password=os.environ.get("CLICKHOUSE_PASSWORD"),
        database="chat",
    ) as client:
        result = client.execute(query)
    return result


def decode_hash_to_query(correct_hash):
    correct_hash = correct_hash.encode("utf-8")
    decoded_bytes = base64.b64decode(correct_hash)
    return decoded_bytes.decode("utf-8")


def test_get_all_messages():
    student_result = student_queries.get_all_messages()
    correct_query = decode_hash_to_query(correct_hash_1)
    expected_result = query_clickhouse(correct_query)
    assert student_result == expected_result


def test_get_top_active_users():
    student_result = student_queries.get_top_active_users()
    correct_query = decode_hash_to_query(correct_hash_2)
    expected_result = query_clickhouse(correct_query)
    assert student_result == expected_result


def test_get_average_message_gap():
    student_result = student_queries.get_average_message_gap()
    correct_query = decode_hash_to_query(correct_hash_3)
    expected_result = query_clickhouse(correct_query)
    assert student_result == expected_result


correct_hash_2 = "U0VMRUNUIHVzZXJuYW1lLCBDT1VOVCgqKSBhcyBtZXNzYWdlX2NvdW50CiAgICBGUk9NIHVzZXJfbWVzc2FnZXMKICAgIEdST1VQIEJZIHVzZXJuYW1lCiAgICBPUkRFUiBCWSBtZXNzYWdlX2NvdW50IERFU0MKICAgIExJTUlUIDU7"

correct_hash_1 = "U0VMRUNUICogRlJPTSB1c2VyX21lc3NhZ2Vz"

correct_hash_3 = "V0lUSCBPcmRlcmVkTWVzc2FnZXMgQVMgKAogICAgICAgIFNFTEVDVCByZWNlaXZlZF9hdAogICAgICAgIEZST00gdXNlcl9tZXNzYWdlcwogICAgICAgIE9SREVSIEJZIHJlY2VpdmVkX2F0CiAgICApCgogICAgLCBUaW1lc0FycmF5IEFTICgKICAgICAgICBTRUxFQ1QgZ3JvdXBBcnJheShyZWNlaXZlZF9hdCkgQVMgdGltZXMKICAgICAgICBGUk9NIE9yZGVyZWRNZXNzYWdlcwogICAgKQoKICAgICwgRGlmZmVyZW5jZXMgQVMgKAogICAgICAgIFNFTEVDVAogICAgICAgICAgICBhcnJheU1hcCgoeCwgeSkgLT4gdG9JbnQzMih5IC0geCksIGFycmF5U2xpY2UodGltZXMsIDEsIGxlbmd0aCh0aW1lcyktMSksIGFycmF5U2xpY2UodGltZXMsIDIpKSBBUyBkaWZmcwogICAgICAgIEZST00gVGltZXNBcnJheQogICAgKQoKICAgIFNFTEVDVCBBVkcoZGlmZmVyZW5jZSkgQVMgYXZnX3RpbWVfZ2FwX3NlY29uZHMKICAgIEZST00gRGlmZmVyZW5jZXMKICAgIEFSUkFZIEpPSU4gZGlmZnMgQVMgZGlmZmVyZW5jZTs="
