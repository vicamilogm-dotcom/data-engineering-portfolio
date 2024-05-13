import great_expectations as gx
import pandas as pd
import requests
import os


def send_message(message: str):
    """
    Sends a message to the Wagon Chat channel.

    This function posts a message to the Wagon Chat channel specified by the environment variable `LAKE_BUCKET`.
    The message is sent with the author name "ge".

    Parameters:
    ----------
    message : str
        The content of the message to be sent to the chat channel.

    Returns:
    -------
    None

    Raises:
    ------
    HTTPError:
        If the post request to the chat channel fails.
    """
    base_url = "https://chat.api.lewagon.com"
    channel = os.environ["LAKE_BUCKET"]
    url = f"{base_url}/{channel}/messages"

    data = dict(author="ge", content=message)
    response = requests.post(url, data=data)
    response.raise_for_status()


def run_expectations(df: pd.DataFrame):
    """
    Validates a given DataFrame against a predefined set of expectations using Great Expectations.

    The function performs the following steps:
    1. Gets the current Great Expectations context.
    2. Adds or updates a pandas datasource.
    3. Adds a dataframe asset to the datasource.
    4. Builds a batch request using the provided DataFrame.
    5. Creates or updates a checkpoint for validation.
    6. Runs the checkpoint and captures the result.
    7. Builds data documentation.
    8. Iterates through the validation results to check for failures.
    9. Sends appropriate messages based on the validation outcome.

    Parameters:
    ----------
    df : pd.DataFrame
        The pandas DataFrame to be validated.

    Returns:
    -------
    None
    """
    pass  # YOUR CODE HERE
