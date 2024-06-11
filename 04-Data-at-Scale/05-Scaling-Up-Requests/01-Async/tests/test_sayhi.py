import time
import pandas as pd
from lwasync import client_asynchronous
from lwasync import client_synchronous


def test_sync_one():
    response = client_synchronous.make_one_call(index=0)
    assert isinstance(response, dict)


def test_sync_many():
    number_of_calls = 2
    responses, _ = client_synchronous.make_many_calls(number_of_calls)
    assert isinstance(responses, pd.DataFrame)
    assert len(responses) == number_of_calls


def test_async_faster():
    number_of_calls = 3
    tsync0 = time.time()
    client_synchronous.generate_statistics_sync(number_of_calls)
    tsync = time.time() - tsync0

    tasync0 = time.time()
    client_asynchronous.generate_statistics_async(number_of_calls)
    tasync = time.time() - tasync0

    assert (
        tsync > tasync
    ), "Are your async and sync methods testing the same API endpoint?"
