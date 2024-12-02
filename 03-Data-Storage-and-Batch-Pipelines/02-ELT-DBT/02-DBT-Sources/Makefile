.PHONY: test_stg_raw_sales test_stg_raw_product_ship test

include ../../../make.inc

test_stg_raw_sales:
	pytest -v --disable-warnings tests/test_stg_raw_sales.py

test_stg_raw_product_ship:
	pytest -v --disable-warnings tests/test_stg_raw_product_ship.py

test: pytest-and-write-output
