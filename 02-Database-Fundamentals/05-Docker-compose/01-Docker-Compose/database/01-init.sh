#!/bin/bash
set -e

# 💡 Let's first connect to postgres with default admin postgres credentials...
psql -v --username "postgres" --dbname "postgres" <<-EOSQL
  /* ...in order to create our own admin user and custom DB for this challenge */
  CREATE USER $APP_DB_USER WITH PASSWORD '$APP_DB_PASS';
  CREATE DATABASE $APP_DB_NAME;
  GRANT ALL PRIVILEGES ON DATABASE $APP_DB_NAME TO $APP_DB_USER;
EOSQL

# ☝️ Whatever is between the two "EOSQL" is going to be passed
# as standard input to the command before!
# This is called the "heredoc" syntax in bash scripting.
