# 🎯 Goal

Metabase is a popular open-source business intelligence (BI) tool that provides a user-friendly interface for querying databases, creating visualizations, generating reports, and interactive dashboards. The free, open-source version can do many things that other paid BI tools like PowerBI, Looker Studio, and Tableau can do with the caveat that you need to self-host it. Metabase does have fully managed, cloud based products, using a business model similar to dbt.

For a self hosted use case, it's more common to make internally facing dashboards and reports for your company, than externally facing visualisations for clients or a B2C market.

To use Metabase, you will need to set it up using docker-compose and connect it to a Postgres database. As a data engineer, it is important for you to be able to set up the environment and connect the database 💪, even if you may not be the one creating the dashboards 📊.

The goal of this challenge is to get a simple dashboard up by loading some F1 data.

<br>

# 1️⃣ Downloading Data

Run the following command to download a `SQL` file and place it in your `database/init/` subdirectory:

```bash
curl --output ./database/init/f1db.sql.gz https://storage.googleapis.com/lewagon-data-engineering-bootcamp-assets/datasets/f1/f1db.sql.gz
```

The SQL file is still in a zipped archive, unzip it using the `gzip` command from the terminal. Make sure it's named `f1db.sql.init` in the `database/init/` folder.

<br>

# 2️⃣ Getting Metabase running

The `docker-compose.yml` file has been provided for you! Have a read through, make sure that you understand the different services and the environment variables.

❓ Why does Metabase need a postgres database?

❓ Why is their two postgres databases?

Metabase needs a database for persistence of data for its metadata, the same reason why Airflow needs a database as well. Metabase needs to store its own configuration data, settings, user accounts, permissions, as well as saved queries and even the locations and types of visualisations you have!

It's considered bad practice to use metadata databases as data stores. This is a great example of the [separation of concerns](https://en.wikipedia.org/wiki/Separation_of_concerns). The sole purpose of the metadata database is to hold metadata. This allows you to connect to other data sources (postgres/BigQuery/ClickHouse/etc) for your analytics needs.

## 2.1. Postgres initialisation

We have set `POSTGRES_DB` and `POSTGRES_USER` for each postgres service so that for each postgres instance, the corresponding user and database will be created. Metabase will handle the creation of databases and tables in the metadata database, but we'll need an `init` script to handle the loading of the Formula 1 data.

Luckily we have already have one: `f1db.sql`. This (very long) SQL script contains all the commands to create tables and insert data for our Formula 1 database.

<details>
<summary markdown='span'>💡 How do postgres init scripts work</summary>

When postgres initialises (or runs for the first time), it will execute SQL and shell scripts found in `/docker-entrypoint-initdb.d/` (mounted to `database/init/` on our VM's file system) in **alphabetical order**. You may see init scripts numbered to make the execution order explicit.

Note that it will only execute **shell scripts** (`.sh`) and **SQL** (`.sql`) scripts. If you have files with different extensions, they will not be executed.

If you have multiple postgres instances in a container stack, it's common to have a separate folder with initialisation scripts to mount to each instance.
</details>

## 2.2. Docker compose

Make sure to create a `.env` file with a `POSTGRES_PASSWORD` and `F1_DB_PASSWORD` from the `.env.sample`. Then to get Metabase up and running:

```bash
docker compose up
```

## 2.3. Logging in and creating connection

Log into Metabase and load the Postgres database as a source using the environment variables that you included in the docker-compose file.

Verify that the data has been loaded. It should be under `Browse Data` ➡️ `Postgres`. You should see the `drivers` table, as well as many more.

## 2.4. Stateful containers

We are using **Docker volumes** here to maintain state in our databases. If you forgot to reload your `.env` before spinning up you container stack, you may get an error with the postgres initialisation.

To do a full teardown, you'll need bring down your container stack, remove the docker managed volumes, then spin up the containers stack again.

To view docker managed volumes:

```bash
docker volume list
```

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

There are no tests for this challenge, but make sure to git add, commit, and push your code to Github!

<br>
