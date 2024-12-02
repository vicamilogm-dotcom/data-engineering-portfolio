.PHONY: test_mart_user test

include ../../../make.inc

test_mart_user:
	pytest -v --disable-warnings tests/test_mart_user.py

test: pytest-and-write-output
