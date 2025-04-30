#!/usr/bin/env bash
set -x

echo "Adding postgres warehouse connection"
airflow connections add 'pg_warehouse_connection' \
                    --conn-type postgres \
                    --conn-host "postgres_warehouse" \
                    --conn-schema "$WAREHOUSE_DB" \
                    --conn-login "$WAREHOUSE_USER" \
                    --conn-password "$WAREHOUSE_PASSWORD" \
                    --conn-port "5432"
