# Metabase
To use Metabase, you will need to set it up using docker-compose and connect it to a Postgres database. As a data engineer, it is important for you to be able to set up the environment and connect the database 💪, even if you may not be the one creating the dashboards 📊.

### Instructions
1️⃣ ❓ Run the following command to download a `SQL` file and place it in your `database/init/` subdirectory:
```bash
curl --output ./database/init/f1db.sql.gz https://storage.googleapis.com/lewagon-data-engineering-bootcamp-assets/datasets/f1/f1db.sql.gz
```

2️⃣ ❓ The sql file is still zipped, unzip it yourself using the `gzip` command from the terminal.

3️⃣ 😁 The docker-compose.yml file has been created for you!

4️⃣ ❓ Run `docker compose up`

5️⃣ ❓ Log into Metabase

6️⃣ ❓ Load the postgres database as a source using the environment variables that you included in the docker-compose file.

7️⃣ ❓ Verify that the data has been loaded. It should be under `Browse Data` ➡️ `Postgres`. You should amongst other see the `drivers` table.

8️⃣ ❓ Have a look at the tables that the `f1db.sql` file created. These tables are included:
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

🚀 In the next challenge you will use these tables to write a Streamlit application, so take some time to discover each table!
