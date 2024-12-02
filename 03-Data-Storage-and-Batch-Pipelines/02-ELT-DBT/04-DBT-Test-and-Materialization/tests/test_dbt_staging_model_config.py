import pathlib
import yaml

challenge_level_dir = pathlib.Path(__file__).parent.parent
models_config = (
    challenge_level_dir / "dbt_lewagon/models/staging/staging_models.yml"
).resolve()


with open(models_config) as f:
    staging_models_yml = yaml.safe_load(f)


def test_staging_models_file_created():
    assert models_config.is_file(), "staging_models.yml has not been created"
    assert (
        staging_models_yml.get("models") is not None
    ), "staging_models.yml should have a 'models' key"


def test_staging_models_file_populated():
    # Models present
    expected_models = set(["stg_raw_sales", "stg_raw_product", "stg_raw_ship"])
    found_models = set([table["name"] for table in staging_models_yml["models"]])

    assert (
        expected_models == found_models
    ), "Missing one or more models from staging_models.yml"

    # Columns
    expected_columns = {
        "stg_raw_sales": set(
            [
                "date_date",
                "orders_id",
                "products_id",
                "revenue",
                "quantity",
            ]
        ),
        "stg_raw_product": set(
            [
                "products_id",
                "purchase_price",
            ]
        ),
        "stg_raw_ship": set(
            [
                "orders_id",
                "shipping_fee",
                "log_cost",
                "ship_cost",
            ]
        ),
    }
    for model in staging_models_yml["models"]:
        if model["name"] in expected_columns.keys():
            found_columns = set([val["name"] for val in model["columns"]])
            assert (
                expected_columns[model["name"]] == found_columns
            ), f"Missing columns in {model['name']}"
        else:
            assert False, "Missing a model from staging_models.yml"

    # Descriptions
    for model in staging_models_yml["models"]:
        if model["name"] in expected_columns.keys():
            found_num_descriptions = len(
                [
                    val.get("description")
                    for val in model["columns"]
                    if val.get("description") is not None
                ]
            )
            expected_len_descriptions = len(expected_columns[model["name"]])
            assert (
                expected_len_descriptions == found_num_descriptions
            ), f"Missing description from {model['name']}"
