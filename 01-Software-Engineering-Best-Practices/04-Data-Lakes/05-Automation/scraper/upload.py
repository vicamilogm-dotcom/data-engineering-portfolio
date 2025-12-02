from datetime import datetime
from google.cloud import storage
import os


def upload_to_lake(file_name) -> str:
    """
    Uploads a file to a GCP bucket, organizing it in a data lake's raw zone with a date-based structure.

    Args:
    - file_name (str): The name of the file to upload.

    Returns:
    - blob_path (str): The path of the file in the data lake.
    """
    date_today = datetime.now()
    year = date_today.strftime("%Y")
    month = date_today.strftime("%m")
    day = date_today.strftime("%d")

    blob_path = f"raw/hackernews/stories/{year}/{month}/{day}/{file_name}"

    storage_client = storage.Client()

    bucket_name = os.environ["LAKE_BUCKET"]
    bucket = storage_client.bucket(bucket_name)

    blob = bucket.blob(blob_path)
    blob.upload_from_filename(file_name)
    print(f"File {file_name} uploaded to {blob_path}")
    return blob_path
