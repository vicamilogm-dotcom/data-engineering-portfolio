#!/bin/bash

set -e

psql -v --username "$APP_DB_USER" --dbname "$APP_DB_NAME" -f /docker-entrypoint-initdb.d/f1db.sql.init
