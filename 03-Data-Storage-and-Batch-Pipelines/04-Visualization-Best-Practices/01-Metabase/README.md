# 🎯 Goal

Metabase is a popular open-source business intelligence (BI) tool that provides a user-friendly interface for querying databases, creating visualizations, generating reports, and interactive dashboards. The free, open-source version can do many things that other paid BI tools like PowerBI, Looker Studio, and Tableau can do with the caveat that you need to self-host it. Metabase does have fully managed, cloud based products, using a business model similar to dbt.

For a self hosted use case, it's more common to make internally facing dashboards and reports for your company, than externally facing visualisations for clients or a B2C market.

To use Metabase, you will need to set it up using docker-compose and connect it to a Postgres database. As a data engineer, it is important for you to be able to set up the environment and connect the database 💪, even if you may not be the one creating the dashboards 📊.

The goal of this challenge is to get a simple dashboard up by loading some F1 data.

<br>

# 1️⃣ Downloading Data

Run the following command to download a `SQL` file and place it in your `database/init/` subdirectory:

```bash
curl --output ./database/init/f1db.sql.init.gz https://storage.googleapis.com/lewagon-data-engineering-bootcamp-assets/datasets/f1/f1db.sql.gz
```

The SQL file is still in a zipped archive, unzip it using the `gzip` command from the terminal. Make sure it's named `f1db.sql.init` in the `database/init/` folder.

<br>

# 2️⃣ Getting Metabase running

The `docker-compose.yml` file has been provided for you! Have a read through, make sure that you understand the different services and the environment variables.

❓ Why does Metabase need a postgres database?

Metabase needs a database for persistence of data for its metadata, the same reason why Airflow needs a database as well. Metabase needs to store its own configuration data, settings, user accounts, permissions, as well as saved queries and even the locations and types of visualisations you have!

We'll also be loading our F1 Data into this postgres instance. In production, you would read from an externally hosted database or warehouse to keep the compute and memory load on the machine hosting Metabase low.

## 2.1. Postgres init script

When we start our postgres container for the first time it will use a combination of **environment variables** and SQL scripts located in `/docker-entrypoint-initdb.d/` (mounted to `database/init/` on our VM's file system) to create initial users, databases, and tables.

We have set our `POSTGRES_DB` and `POSTGRES_USER` in our `docker-compose.yml` so postgres' will create the corresponding user and database in the postgres instance - fantastic! It will create our Metabase metadata DB! But we still don't have a database to hold our Formula 1 data 😢

If our `f1db.sql.init` file was named: `f1db.sql`, postgres will execute that script against the default user AND database, mixing our analytics data and service metadata together in the same database - that's a big no no!

We have created a short init script: `01-init-f1.sh`, to create a database to hold our F1 data, and grant privilege to our user to read that data - check it out!

❓ **So why are you telling me this?**

When postgres initialises, it will execute the SQL and shell scripts in `/docker-entrypoint-initdb.d/` (mounted to `database/init/` on our VM's file system) in **alphabetical order**. This is use super useful to know if you're creating more than one database. Because our `f1db` file doesn't end with `.sql`, it won't be executed on initialisation.

## 2.2. Docker compose

Make sure to create a `.env` file with a `POSTGRES_PASSWORD`, then to get Metabase up and running:

```bash
docker compose up
```

## 2.3. Logging in and creating connection

Log into Metabase

Load the Postgres database as a source using the environment variables that you included in the docker-compose file, and the database you created with your init script.

Verify that the data has been loaded. It should be under `Browse Data` ➡️ `Postgres`. You should amongst other see the `drivers` table.

<br>

# 3️⃣ Look around!

Have a look at the tables that the `f1db.sql` file created. These tables are included:
- races
- circuits
- constructor_results
- constructor_standings
- constructors
- driver_standings
- drivers
- lap_times
- pit_stops
- qualifying
- results
- seasons
- status

Feel free to create some visualisations!

<br>

# 🏁 Finishing up

🚀 In the next challenge you will use these tables to write a Streamlit application, so take some time to discover each table!

There are no tests for this challenge, but make sure to git add, commit, and push your code to github!

<br>
