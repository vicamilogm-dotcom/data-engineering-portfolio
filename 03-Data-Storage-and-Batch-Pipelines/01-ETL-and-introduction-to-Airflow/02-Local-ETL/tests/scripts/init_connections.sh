#!/usr/bin/env bash
set -x

echo "Add connection"
airflow connections add 'sqlite_connection' \
                    --conn-type sqlite \
                    --conn-host "$PWD/tests/temp/airflow.db"
