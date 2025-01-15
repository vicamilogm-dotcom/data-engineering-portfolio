.PHONY: test_setup test_dag_config test_tasks_configs test_python_functions test

# Our tests will re-create a SQLite copy of your postgres db inside the "temp" folder, and then test against this sqlite db
AIRFLOW_HOME=${PWD}/tests/temp

test_setup:
	pytest -v tests/test_setup.py

test_dag_config:
	export AIRFLOW_HOME=${AIRFLOW_HOME}; \
	airflow db migrate; \
	pytest -v tests/test_dag_config.py

test_tasks_configs:
	export AIRFLOW_HOME=${PWD}/tests/temp; \
	airflow db migrate; \
	pytest -v tests/test_tasks_configs.py

test_python_functions:
	pytest -v tests/test_python_functions.py

test:
	export AIRFLOW_HOME=${AIRFLOW_HOME}; \
	airflow db migrate; \
	pytest tests -m "not optional" -v 2>&1 > test_output.txt || echo "-- Some tests didn't pass, let's look at the output"; \
	pytest tests -m "not optional" -v --color=yes
