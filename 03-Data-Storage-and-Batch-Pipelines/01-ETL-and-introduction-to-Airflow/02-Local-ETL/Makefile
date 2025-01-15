.PHONY: test_dag_config test_tasks_configs test_python_functions test

# The tests will create a SQLite copy of your postgres db inside the "temp" folder, and then test against this sqlite db
AIRFLOW_HOME=${PWD}/tests/temp

test_dag_config:
	export AIRFLOW_HOME=${AIRFLOW_HOME}; \
	airflow db migrate; \
	chmod +x tests/scripts/init_connections.sh; tests/scripts/init_connections.sh; echo 'Succesfully created db and connection'; \
	pytest -v --disable-warnings tests/test_dag_config.py

test_tasks_configs:
	export AIRFLOW_HOME=${AIRFLOW_HOME}; \
	airflow db migrate; \
	chmod +x tests/scripts/init_connections.sh; tests/scripts/init_connections.sh; echo 'Succesfully created db and connection'; \
	pytest -v --disable-warnings tests/test_tasks_configs.py

test_python_functions:
	export AIRFLOW_HOME=${AIRFLOW_HOME}; \
	airflow db migrate; \
	chmod +x tests/scripts/init_connections.sh; tests/scripts/init_connections.sh; echo 'Succesfully created db and connection'; \
	pytest -v --disable-warnings tests/test_python_functions.py

test:
	export AIRFLOW_HOME=${AIRFLOW_HOME}; \
	airflow db migrate; \
	chmod +x tests/scripts/init_connections.sh; tests/scripts/init_connections.sh; echo 'Succesfully created db and connection'; \
	pytest tests -m "not optional" -v --disable-warnings 2>&1 > test_output.txt || echo "-- Some tests didn't pass, let's look at the output"; \
	pytest tests -m "not optional" -v --disable-warnings --color=yes
