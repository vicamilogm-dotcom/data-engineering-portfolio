from pipeline.schemas import bigquery_schemas
from google.cloud import bigquery


def main():
    """
    Main function to take the bigquery schemas and create the tables in the raw dataset.
    """
    client = bigquery.Client()
    dataset_name = "adventure_works_raw"

    for table_name, schema in bigquery_schemas.items():
        pass  # YOUR CODE HERE


if __name__ == "__main__":
    main()
