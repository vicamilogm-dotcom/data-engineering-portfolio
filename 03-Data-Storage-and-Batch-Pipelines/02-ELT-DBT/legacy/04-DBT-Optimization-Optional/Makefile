.PHONY: test_dbt_project_created test_dbt_variable_created test

include ../../../make.inc

test_dbt_project_created:
	pytest -v --disable-warnings tests/test_dbt_project_created.py

test_dbt_variable_created:
	pytest -v --disable-warnings tests/test_dbt_variable_created.py


test: pytest-and-write-output
