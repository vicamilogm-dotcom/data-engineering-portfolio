import os
import yaml
import lewagonde

dbt_profile_path = lewagonde.DBT_PROFILE_PATH
dbt_full_profile_path = os.path.expanduser(dbt_profile_path)

with open(dbt_full_profile_path) as f:
    profile_dict = yaml.safe_load(f)


def test_dbt_profile_location():
    assert os.path.exists(
        dbt_full_profile_path
    ), "Your profiles.yml file is not located in the correct folder. It should be under ~/.dbt/"


def test_dbt_profile_name():
    assert "dbt_lewagon" in profile_dict, "Your profile is not called dbt_lewagon"


def test_dbt_correct_keys():
    assert (
        "outputs" in profile_dict["dbt_lewagon"]
    ), "outputs should be below dbt_lewagon"
    assert (
        "dev" in profile_dict["dbt_lewagon"]["outputs"]
    ), "dev should be one of your defined targets"
    assert (
        "dataset" in profile_dict["dbt_lewagon"]["outputs"]["dev"]
    ), "within the dev target, the key 'dataset' should be defined"


def test_dbt_profile_dataset():
    dataset = profile_dict["dbt_lewagon"]["outputs"]["dev"]["dataset"]
    assert dataset.startswith("dbt_"), "Your dataset should start with 'dbt_'"
    assert dataset.endswith("_day1"), "Your dataset should end with '_day1'"


def test_dbt_profile_other_keys():
    dev = profile_dict["dbt_lewagon"]["outputs"]["dev"]
    assert dev["location"] == "US", "Location is wrong"
    assert dev["method"] == "service-account", "Method is wrong"
    assert dev["priority"] == "interactive", "Priority is wrong"
    # TODO: parse the service account GCP file, to extract their own project ID
    # (while for IKEA, it was a shared one, so it could be hardcoded)
    # assert dev["project"] == 'ingka-data-engineering-dev', "Project is wrong"
    assert dev["threads"] == 1, "Threads is wrong"
    assert dev["type"] == "bigquery", "Type is wrong"
    assert (
        "/.gcp_keys" in dev["keyfile"] and ".json" in dev["keyfile"]
    ), "Path for keyfile is incorrect"
