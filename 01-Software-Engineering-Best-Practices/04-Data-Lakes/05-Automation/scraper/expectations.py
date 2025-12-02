import great_expectations as gx
import pandas as pd
import requests
import os


def send_message(message: str):
    """
    Send a message to the Wagon Chat channel.
    """
    base_url = "https://chat.api.lewagon.com"
    channel = os.environ["LAKE_BUCKET"]
    url = f"{base_url}/{channel}/messages"

    data = dict(author="ge", content=message)
    response = requests.post(url, data=data)
    response.raise_for_status()


def run_expectations(df: pd.DataFrame):
    context = gx.get_context()
    datasource = context.sources.add_or_update_pandas(name="hn_df")
    data_asset = datasource.add_dataframe_asset(name="hn_df")
    batch_request = data_asset.build_batch_request(dataframe=df)
    checkpoint = context.add_or_update_checkpoint(
        name="check_hn",
        validations=[
            {
                "batch_request": batch_request,
                "expectation_suite_name": "hn_expectation_suite",
            }
        ],
    )
    checkpoint_result = checkpoint.run()
    context.build_data_docs()
    failures = []
    for expectation_result in next(iter(checkpoint_result["run_results"].values()))[
        "validation_result"
    ]["results"]:
        if not expectation_result["success"]:
            failures.append(expectation_result)
    if failures:
        for failure in failures:
            send_message("Expectation failed!")
            send_message(failure["expectation_config"]["kwargs"]["column"])
            send_message(str(failure["result"]))
    else:
        send_message("All expectations passed!")
