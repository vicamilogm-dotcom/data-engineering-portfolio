from google.cloud import bigquery
from pipeline.schemas import bigquery_schemas
import os


def rename_type_to_field_type(schema_dict):
    for _, fields in schema_dict.items():
        for field in fields:
            if "type" in field:
                field["field_type"] = field.pop("type")
    return schema_dict


def main():
    client = bigquery.Client()

    dataset_name = os.environ.get("BIGQUERY_DATASET")

    updated_schemas = rename_type_to_field_type(bigquery_schemas)

    for table_name in bigquery_schemas.keys():
        pass  # YOUR CODE HERE


if __name__ == "__main__":
    main()
