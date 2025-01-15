.PHONY: test_extract_dag test_transform_dag test_load_dag test

# Our tests will re-create a SQLite copy of your postgres db inside the "temp" folder, and then test against this sqlite db
AIRFLOW_HOME=${PWD}/tests/temp


test_extract_dag:
	export AIRFLOW_HOME=${AIRFLOW_HOME}; \
	poetry run airflow db migrate; \
	chmod +x tests/scripts/init_connections.sh; poetry run tests/scripts/init_connections.sh; echo 'Succesfully created db and connection'; \
	pytest tests/test_extract_dag.py -v --color=yes --disable-warnings

test_transform_dag:
	export AIRFLOW_HOME=${AIRFLOW_HOME}; \
	poetry run airflow db migrate; \
	chmod +x tests/scripts/init_connections.sh; poetry run tests/scripts/init_connections.sh; echo 'Succesfully created db and connection'; \
	pytest tests/test_transform_dag.py -v --color=yes --disable-warnings

test_load_dag:
	export AIRFLOW_HOME=${AIRFLOW_HOME}; \
	poetry run airflow db migrate; \
	chmod +x tests/scripts/init_connections.sh; poetry run tests/scripts/init_connections.sh; echo 'Succesfully created db and connection'; \
	pytest tests/test_load_dag.py -v --color=yes --disable-warnings

test:
	export AIRFLOW_HOME=${AIRFLOW_HOME}; \
	poetry run airflow db migrate; \
	chmod +x tests/scripts/init_connections.sh; poetry run tests/scripts/init_connections.sh; echo 'Succesfully created db and connection'; \
	pytest tests -m "not optional" -v --disable-warnings 2>&1 > test_output.txt || echo "-- Some tests didn't pass, let's look at the output"; \
	pytest tests -m "not optional" -v --disable-warnings --color=yes
