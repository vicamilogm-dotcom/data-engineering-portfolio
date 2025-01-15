#!/bin/bash

set -e

# 💡 Let's first connect to postgres with default admin postgres credentials...
psql -v --username "$POSTGRES_USER" --dbname "postgres" <<-EOSQL
  CREATE DATABASE $DATA_DB_NAME;
  GRANT ALL PRIVILEGES ON DATABASE $DATA_DB_NAME TO $POSTGRES_USER;
EOSQL

# ☝️ Whatever is between the two "EOSQL" is going to be passed
# as standard input to the command before!
# This is called the "heredoc" syntax in bash scripting.


# Connect to F1 db and load data from file
psql -v --username "$POSTGRES_USER" --dbname "$DATA_DB_NAME" -f /docker-entrypoint-initdb.d/f1db.sql.init
