import pathlib
import yaml

challenge_level_dir = pathlib.Path(__file__).parent.parent
models_config = (
    challenge_level_dir / "dbt_lewagon/models/intermediate/intermediate_models.yml"
).resolve()
packages_path = (challenge_level_dir / "dbt_lewagon/packages.yml").resolve()

with open(models_config) as f:
    int_models_yml = yaml.safe_load(f)


def test_intermediate_models_file_created():
    assert models_config.is_file(), "intermediate_models.yml has not been created"
    assert (
        int_models_yml.get("models") is not None
    ), "intermediate_models.yml should have a 'models' key"


def test_intermediate_models_file_populated():
    # Models present
    expected_models = set(
        ["int_sales_margin", "int_orders_margin", "int_orders_operational"]
    )
    found_models = set([table["name"] for table in int_models_yml["models"]])

    assert (
        expected_models == found_models
    ), "Missing one or more models from intermediate_models.yml"

    # Columns
    expected_columns = {
        "int_sales_margin": set(
            [
                "products_id",
                "orders_id",
                "date_date",
                "revenue",
                "quantity",
                "purchase_price",
                "purchase_cost",
                "margin",
            ]
        ),
        "int_orders_margin": set(
            [
                "orders_id",
                "date_date",
                "revenue",
                "quantity",
                "purchase_cost",
                "margin",
            ]
        ),
        "int_orders_operational": set(
            [
                "orders_id",
                "date_date",
                "operational_margin",
                "quantity",
                "revenue",
                "purchase_cost",
                "margin",
                "shipping_fee",
                "log_cost",
                "ship_cost",
            ]
        ),
    }
    for model in int_models_yml["models"]:
        if model["name"] in expected_columns.keys():
            found_columns = set([val["name"] for val in model["columns"]])
            assert (
                expected_columns[model["name"]] == found_columns
            ), f"Missing columns in {model['name']}"
        else:
            assert False, "Missing a model from intermediate_models.yml"

    # Descriptions
    for model in int_models_yml["models"]:
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


def test_packages_created():
    assert packages_path.is_file(), "packages.yml has not been created"


def test_int_sales_margin_tests():
    int_sales = [
        value
        for value in int_models_yml["models"]
        if value.get("name") == "int_sales_margin"
    ][0]["columns"]

    # in built tests
    expected_tests_per_column = {
        "products_id": 1,
        "orders_id": 1,
    }
    num_tests_per_column = {}
    for column in int_sales:
        num_tests_per_column[column["name"]] = (
            0 if column.get("data_tests") is None else len(column.get("data_tests"))
        )
    for col, num_tests in expected_tests_per_column.items():
        assert (
            num_tests == num_tests_per_column[col]
        ), f"Column: {col} has the incorrect number of tests"

    # db_utils test
    data_tests = [
        value
        for value in int_models_yml["models"]
        if value.get("name") == "int_sales_margin"
    ][0].get("data_tests")
    assert (
        data_tests is not None
    ), "data_tests key not found for model int_sales_margin at model level"
    assert (
        list(data_tests[0].keys())[0] == "dbt_utils.unique_combination_of_columns"
    ), "dbt_utils.unique_combination_of_columns is not a key in data_tests"

    expected_combination = set(["orders_id", "products_id"])
    found_combination = set(
        data_tests[0]["dbt_utils.unique_combination_of_columns"].get(
            "combination_of_columns"
        )
    )
    assert (
        expected_combination == found_combination
    ), "Incorrect combination of columns found"


def test_int_orders_margin_tests():
    int_orders_margin = [
        value
        for value in int_models_yml["models"]
        if value.get("name") == "int_orders_margin"
    ][0]["columns"]

    # in built tests
    expected_tests_per_column = {
        "orders_id": 2,
    }
    num_tests_per_column = {}
    for column in int_orders_margin:
        num_tests_per_column[column["name"]] = (
            0 if column.get("data_tests") is None else len(column.get("data_tests"))
        )
    for col, num_tests in expected_tests_per_column.items():
        assert (
            num_tests == num_tests_per_column[col]
        ), f"Column: {col} has the incorrect number of tests"


def test_int_orders_operational_tests():
    int_orders_operational = [
        value
        for value in int_models_yml["models"]
        if value.get("name") == "int_orders_operational"
    ][0]["columns"]

    # in built tests
    expected_tests_per_column = {
        "orders_id": 2,
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


if __name__ == "__main__":
    from pprint import pprint

    # int_sales = [value for value in int_models_yml["models"] if value.get("name") == "int_sales_margin"][0]["columns"]
    data_tests = [
        value
        for value in int_models_yml["models"]
        if value.get("name") == "int_sales_margin"
    ][0].get("data_tests")[0]
    pprint(data_tests)
