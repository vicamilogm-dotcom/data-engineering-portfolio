from pipeline.schemas import bigquery_schemas
from google.cloud import bigquery
import os


def main():
    """
    Main function to take the bigquery schemas and create the tables in the raw dataset.
    """
    client = bigquery.Client()
    dataset_name = os.environ.get("BIGQUERY_DATASET")

    for table_name, schema in bigquery_schemas.items():
        pass  # YOUR CODE HERE


if __name__ == "__main__":
    main()
