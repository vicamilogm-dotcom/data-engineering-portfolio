import base64
import json
import os
from typing import Any, Dict, List

import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account


def get_client():
    """
    Returns a BigQuery client, assuming the credentials are stored in a JSON file located at the value
    of the environment variable `GCP_CREDS_JSON`
    """
    creds_dict = json.loads(base64.b64decode(os.environ.get("GCP_CREDS_JSON_BASE64")))

    credentials = service_account.Credentials.from_service_account_info(
        creds_dict, scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )

    return bigquery.Client(credentials=credentials, project=credentials.project_id)


def query_as_list(
    client, query: str, query_parameters: List[bigquery.ScalarQueryParameter] = None
) -> List[Dict[str, Any]]:
    """
    Given a BigQuery client, and a query string, runs the query and inject the result into a Pandas DataFrame.
    """
    if query_parameters is None:
        query_parameters = []
    job_config = bigquery.QueryJobConfig(query_parameters=query_parameters)

    query_job = client.query(query, job_config=job_config)

    iterator = query_job.result(timeout=30)

    return list(iterator)


def query_as_df(
    client, query: str, query_parameters: List[bigquery.ScalarQueryParameter] = None
) -> pd.DataFrame:
    """
    Given a BigQuery client, and a query string, runs the query and inject the result into a Pandas DataFrame.
    """
    rows = query_as_list(client=client, query=query, query_parameters=query_parameters)

    return pd.DataFrame(
        data=[list(row.values()) for row in rows], columns=list(rows[0].keys())
    )
