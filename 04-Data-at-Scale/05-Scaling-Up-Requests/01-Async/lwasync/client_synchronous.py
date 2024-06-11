from typing import Any, Dict, List
import time
import pandas as pd

# The library to make synchronous HTTP requests
import requests


def make_one_call(index) -> Dict[str, Any]:
    """
    Make one call to the API's /say-hi endpoint
    """
    response = None
    t0 = time.time()
    # Replace `None` by a call to the API, using the `requests` library
    # YOUR CODE HERE
    duration_seconds = time.time() - t0
    return {**response, "index": index, "duration_seconds": duration_seconds}


def make_many_calls(number: int) -> List[Dict[str, Any]]:
    """
    Runs `number` synchronous calls to the local server and returns all the responses in an array
    """
    t0 = time.time()
    responses = []

    # Below write synchronous code with the `requests` library, and append responses to the `responses` array
    # YOUR CODE HERE

    duration_seconds = time.time() - t0
    print(f"It took {duration_seconds} seconds to run the {number} synchronous calls!")
    return pd.DataFrame(responses), duration_seconds


def generate_statistics_sync(number: int = 10):
    """
    The main function to run this file as a standalone program and output /say-hi API endpoint statistics
    """
    # Then we call the function `make_many_calls` with the argument `number`
    return make_many_calls(number)


if __name__ == "__main__":
    # Here we simply call `generate_statistics()` when this file is run as a program and not imported as a library
    generate_statistics_sync()
