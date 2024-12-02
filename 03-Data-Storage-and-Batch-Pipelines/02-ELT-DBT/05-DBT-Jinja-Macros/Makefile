.PHONY: test_sql_macro_file_created test

include ../../../make.inc

test_sql_macro_file_created:
	pytest -v --disable-warnings tests/test_sql_macro_file_created.py

test: pytest-and-write-output
