import os
import pathlib
import re


# Hardcoded
# current_file = '/home/selim/nico/data-engineering-solutions-week2/02-Data-at-Scales/01-ELT-DBT/01-Setup-DBT/tests/test_dbt_model_documentation.py'
# challenge_level_dir =  pathlib.Path(os.path.realpath(current_file)).parent.parent
challenge_level_dir = pathlib.Path(os.path.realpath(__file__)).parent.parent
dbt_lewagon_dir = os.path.join(challenge_level_dir, "dbt_lewagon/")

# Simplifying the structure of the root directories which are extremely long
# Transforming:
#  /home/selim/nico/data-engineering-solutions-week2/02-Data-at-Scales/01-ELT-DBT/dbt_lewagon/models'
# into
# dbt_lewagon/models

all_sub_dir = [x for x in os.walk(dbt_lewagon_dir)]
all_sub_dir_short = [
    (re.sub(r"^.*?dbt_lewagon", "dbt_lewagon", root), dirs, files)
    for (root, dirs, files) in all_sub_dir
]


def test_documentation_file_created():
    mart_structure = [x for x in all_sub_dir_short if x[0] == "dbt_lewagon/models/mart"]

    assert (
        len(mart_structure) == 1
    ), "dbt_lewagon/models/mart directory has not been created"
    if len(mart_structure) == 1:
        assert (
            "models.yml" in mart_structure[0][2]
        ), "models.yml not created in dbt_lewagon/models/mart directory"
