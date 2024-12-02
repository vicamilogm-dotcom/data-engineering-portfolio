
include ../../../make.inc

.PHONY: test
test: pytest-and-write-output

test_staging_config:
	PYTHONWRITEBYTECODE=1 poetry run pytest -v --color=yes --disable-warnings tests/test_dbt_staging_model_config.py

test_intermediate_config:
	PYTHONWRITEBYTECODE=1 poetry run pytest -v --color=yes --disable-warnings tests/test_dbt_int_model_config.py

test_mart_config:
	PYTHONWRITEBYTECODE=1 poetry run pytest -v --color=yes --disable-warnings tests/test_dbt_mart_model_config.py
