# Asynchronous programming in Python is managed by the `asyncio` library
import asyncio

# The library to make asynchronous HTTP requests
import aiohttp

import pandas as pd
from typing import Any, Dict, List
import time


async def make_one_call(
    session: aiohttp.ClientSession, api_url: str, index: int
) -> Dict[str, Any]:
    """
    Make one call to the API
    """
    response = None
    # Replace `None` by a call to the API, using the `aiohttp` library
    # Follow the Client example here: https://docs.aiohttp.org/en/stable/#client-example
    # in the function `async def main``
    # Note that you only need a bit of the code, given that the `session` is already given as an argument of `make_one_call`
    t0 = time.time()
    # YOUR CODE HERE
    duration_seconds = time.time() - t0

    return {**response, "index": index, "duration_seconds": duration_seconds}


async def make_many_calls(api_url: str, number: int) -> List[Dict[str, Any]]:
    """
    Runs `number` asynchronous calls to the local server.
    Returns a list of responses and a total duration
    """
    t0 = time.time()
    responses = []

    async with aiohttp.ClientSession() as session:
        # using asyncio, gather a list of API calls for the event loop to run
        # YOUR CODE HERE

    duration_seconds = time.time() - t0
    print(f"It took {duration_seconds} seconds to run the {number} asynchronous calls!")
    return pd.DataFrame(responses), duration_seconds


def generate_statistics_async(number: int = 10):
    """
    The main function to run this file as a standalone program and output executed API call statistics
    """
    # API url to test
    api_url = ""
    

    # Instead of simply calling the function we're interested in, we let the event loop run it for us
    # So instead of calling `make_many_calls(...)` let's use asyncio:
    # YOUR CODE HERE
