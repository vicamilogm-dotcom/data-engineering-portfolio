import pathlib
import yaml

challenge_level_dir = pathlib.Path(__file__).parent.parent
models_config = (
    challenge_level_dir / "dbt_lewagon/models/mart/mart_models.yml"
).resolve()


with open(models_config) as f:
    mart_models_yml = yaml.safe_load(f)


def test_mart_models_file_created():
    assert models_config.is_file(), "mart_models.yml has not been created"
    assert (
        mart_models_yml.get("models") is not None
    ), "mart_models.yml should have a 'models' key"


def test_mart_models_file_populated():
    # Models present
    expected_models = set(
        [
            "finance_days",
        ]
    )
    found_models = set([table["name"] for table in mart_models_yml["models"]])

    assert (
        expected_models == found_models
    ), "Missing one or more models from mart_models.yml"

    # Columns
    expected_columns = {
        "finance_days": set(
            [
                "date_date",
                "nb_transactions",
                "quantity",
                "revenue",
                "average_basket",
                "margin",
                "operational_margin",
                "purchase_cost",
                "shipping_fee",
                "log_cost",
                "ship_cost",
            ]
        ),
    }
    for model in mart_models_yml["models"]:
        if model["name"] in expected_columns.keys():
            found_columns = set([val["name"] for val in model["columns"]])
            assert (
                expected_columns[model["name"]] == found_columns
            ), f"Missing columns in {model['name']}"
        else:
            assert False, "Missing a model from mart_models.yml"

    # Descriptions
    for model in mart_models_yml["models"]:
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


def test_mart_finance_days_tests():
    int_orders_operational = [
        value
        for value in mart_models_yml["models"]
        if value.get("name") == "finance_days"
    ][0]["columns"]

    # in built tests
    expected_tests_per_column = {
        "date_date": 2,
    }
    num_tests_per_column = {}
    for column in int_orders_operational:
        num_tests_per_column[column["name"]] = (
            0 if column.get("data_tests") is None else len(column.get("data_tests"))
        )
    for col, num_tests in expected_tests_per_column.items():
        assert (
            num_tests == num_tests_per_column[col]
        ), f"Column: {col} has the incorrect number of tests"
