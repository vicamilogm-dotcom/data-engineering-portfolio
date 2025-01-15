After doing the `01-Docker-Compose` exercise, you should by now have a good understanding of a Docker Compose stack, and how to use it to set up a standard web app with a database and a FastAPI web server.

# 🎯 Goal and Context

Remember challenge **Twitter-CRUD** where we built a Twitter fast API connected to a postgres service, both running on our linux VM without containers? Well, this time we'll containerize it. But now that we can coordinate multiple containers, let's spice things up a bit more

Today we'll build a version of the tweets table **partitioned across two APIs**. Let's imagine our app is struggling to manage the load so we want to create **shards** of the tweets table based on the location of the tweet: Users in Europe can be served their tweets locally and the same for users in the USA.

The architecture we are aiming for:

- Our VM will run **Postgres** as a linux service directly without containers: this will be the full database!
- We'll spawn two **Postgres** containers (two shards EU and US of the full db) with the data volume mapped
- Plus two **FastAPI** app containers for the EU and US database.

<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W1D1/sharded-db.png" width=300>

**Sharding you said??**
- When we split a table into several *subsets* that are still part of the same *database*, they are called **partitions**. Partitions are often done by splitting over a particular index (eg. in our case, the user-location column).
- When we distribute each partitions table into different databases, each partition is a standalone database called a **shard**.
- When *sharding* or *partitioning*, there is no physical database centralizing all data somewhere any more! However, we'll still be able to virtually recreate a "full database" in the same way views are just immaterial tables that are created dynamically as you query them.

**Why sharding?**
- Sharding helps us reduce the size of the tables making queries quicker, but can also help us place those tables where they will be accessed (lower latency for users in both regions).
- There are more business applications to sharding. The obvious is more locations, more shards. You could also shard by the time records were created if the most recent records to be the most demanded by users, like tweets!

### Browse `tweets_api` folder rapidly

☝️ Note that it's a simplified version of `020401-Twitter-CRUD`, with less endpoints and data complexity.

- Only one model: `Tweet`
- Two endpoints: `get/tweets/` and `post/tweets/`

We'll leave the complexity of routing EU vs. US requests to web developers (Web Browser gives IP address, which can be geo-localized, then routed to EU or US accordingly).  As Data Engineers, we want to focus on building 2 API containers that connect their respective get/post requests to the respective database shard.

<br>

# 1️⃣ Setup postgres on VM

Lets create a new database on our VM for the exercise.

❓ Read the beginning of challenge [020301-Setup-Postgres](https://github.com/lewagon/data-engineering-challenges/tree/main/02-Database-Fundamentals/03-SQL-Databases/00-Setup) to recall how we created a postgres superuser and password on our VM.

❓ Then, create a database named `tweets` and connect to it with DBeaver:
<details>
<summary markdown='span'>💡 Create db hint</summary>

```bash
# Create db
createdb tweets
```
</details>

<br>

# 2️⃣ Docker compose

Make sure to copy the `.env.sample` to a `.env`. Have a look at the values and don't forget to `direnv reload`!

## 2.1. Networks

❓ In your `docker-compose.yml` add two bridge networks: `europe` &  `usa`.

## 2.2. Databases

❓ In the `docker-compose.yml` create two database postgres services (`us_database`, `eu_database`), one for each network, as below for USA.

<details>
<summary markdown='span'>💡 Example for USA</summary>

```yml
us_database:
  image: postgres:14.2
  restart: on-failure
  healthcheck:
    test: ["CMD", "pg_isready", "-U", "postgres"]
    interval: 5s
    timeout: 5s
    retries: 5
  volumes:
    - ./scripts/:/docker-entrypoint-initdb.d/
  ports:
    - "5401:5432"
  environment:
    - POSTGRES_PASSWORD=$POSTGRES_PASSWORD
    - APP_DB_USER=usa
    - APP_DB_PASS=$DB_US_PASSWORD
    - APP_DB_NAME=ustweets
  networks:
    - usa
```
</details>

Copy for EU and adjust the environment variables, forwarded ports and network name as you see fit! You can always change them later on.

## 2.3. APIs

❓ Create two FastAPI services in your docker-compose: `eu_webapi` and `us_webapi`, refer to the  previous challenge for inspiration.
- Each should be based on the same `dockerfile-fastapi` that is provided
- Each should depend on its respective regional database
- Each should restart on failure
- Each should be only part of their respective regional network
- Each should have `POSTGRES_DATABASE_URL` equals to the connection string to their regional database
- Each should launch the same command to launch a FastAPI server from `tweets_api.main` in port 8000 inside their respective network

**But how are we we going to differentiate behaviour between the US and the EU database then?**

The key is to update the sqlachemy variable __tablename__ attribute in `model.py` so that it can be set dynamically with an environment variable to their respective **regional_db_name**!
```python
__tablename__ = os.environ.get("TWEETS_TABLE", "tweets")
```

```yml
us_webapi:
  environment:
    - TWEETS_TABLE=us_tweets

eu_webapi:
  environment:
    - TWEETS_TABLE=eu_tweets
```

<details>
<summary markdown='span'>🎁 Solution for US - only look if errors pops up!</summary>

```yml
  us_webapi:
    container_name: us_api
    build:
      context: .
      dockerfile: dockerfile-fastapi
    restart: on-failure
    ports:
      - "8001:8000"
    volumes:
      - ./tweets_api:/app/tweets_api
    environment:
      - POSTGRES_DATABASE_URL=postgresql+psycopg2://usa:$DB_US_PASSWORD@us_database:5432/ustweets
      - TWEETS_TABLE=us_tweets
    command: ["uvicorn", "tweets_api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
    networks:
      - usa
    depends_on:
      - us_database
```

</details>

## 2.4. Launch

❓ `docker compose up` and check 🔍:

- `docker ps` should show all **four** containers are up and healthy
- You can connect to the **two** APIs from your local machine
- You can connect to the **three** DB in DBeaver

❗️ Make sure all the ports have been forwarded!

Then we are ready to create our `tweets` main tables and shard it across our other two databases!

<br>

# 3️⃣ Sharding

## 3.1. Setup Foreign Data Wrappers (FDW)

**On our host database (`tweets`)**:

Our first task is to activate the postgres _foreign data wrapper_ extension. This allows us to use new functions to access SQL data on other servers.
```sql
CREATE EXTENSION postgres_fdw;
```

Lets connect to our two foreign servers (`usa` in the following example).  **Specify the dbname and port** depending on what you defined in your compose file! This creates a new SQL object called a server.
```sql
CREATE SERVER usa FOREIGN DATA WRAPPER postgres_fdw
    OPTIONS (host '127.0.0.1', port '5401', dbname 'ustweets');
```

Now login in to the server. Here in the example below, I want my current user `oliver.giles` to be able to execute SQL on the foreign server `usa` as the user `usa` and I also give the password. This means when I am connected to the host database as the `oliver.giles` user I can execute SQL on the usa server SQL database as well ❗️

```sql
CREATE USER MAPPING FOR "oliver.giles" SERVER usa
    OPTIONS (user 'usa', password 'uspassword');
```

You should see the mappings reflected on DBeaver (refresh if needed)!

<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W1D1/foreign_data_wrapper.png" height=300>

## 3.2. Table creation

**on your host db again** we need to create a new table with an additional call: `partition by`, which describes how the database will be partitioned. In this case on the `location` column.

```sql
CREATE TABLE tweets (
	id serial4 NOT NULL,
	"location" varchar NOT NULL,
	"text" varchar NOT NULL,
	owner_id int4 NOT NULL,
	like_count int4 NOT NULL
)
partition by list ("location");
```

**🇺🇸 Logged into the us server**: we need to create a similar table with matching columns! (Be careful with table names!)

```sql
CREATE TABLE us_tweets (
	id serial4 NOT NULL,
	"location" varchar NOT NULL,
	"text" varchar NOT NULL,
	owner_id int4 NOT NULL,
	like_count int4 NOT NULL
);
```

We are now ready to use the SERVER object we created to connect the master table (`tweets`) to this foreign partition!

## 3.3. Connection

**🌐 On our host server again** lets connect the `us_tweets` table to the master `tweets` table and define the condition for which records will be fed into the `us` partition. The following condition will look to see if `usa` is in the `location` column and store the entire record in the `us_tweets` partition!

```sql
CREATE FOREIGN TABLE us_tweets
    PARTITION OF tweets
    FOR VALUES IN ('usa')
    SERVER usa;
```


🇪🇺 Repeat the whole process for Europe in a table `eu_tweets` with location string `europe`, you should see the following:

<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W1D1/partitions_visible.png" height=600>

<br>

# 4️⃣ Testing it all!

1. 🇺🇸 Put yourself in the shoes of an American user and create one new tweet located in "usa" using the American Fast API server `localhost:xxxx/docs` `/POST` request.

2. 🇪🇺 Do the same from the European server as European user

3. 🌐 Head over to your host db on DBeaver and you should see the sharding working!

<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W1D1/sharding_working.png">

```sql
-- You should be access your remote shards from your host db as if they were local tables!
SELECT * FROM us_tweets
UNION
SELECT * FROM eu_tweets
```

👉 Finally, check on your *regional* FastAPI that `/GET` requests only display *regional* tweets in their respective!

<br>

# 5️⃣ Advanced FDW concepts

**default location**

What if you posted something where location is set to "asia"?
Currently, the sharding will break. If data doesn't fit in either partition, we need some default partition for the overflow to go.

```sql
-- This will redirect all other "locations" to this table
CREATE TABLE default_tweets
    PARTITION OF tweets
    DEFAULT;
```

**Materialized import of foreign data**

Instead of simply allowing you to view the data, you can also use the foreign data wrapper to physically import (as opposed to simply connecting a 'view' over the network) other databases once you create the server object...

```sql
IMPORT FOREIGN SCHEMA public
    FROM SERVER <foreign server> INTO public;
```

**FDW to anything!**

Thanks to the numerous [open-source FDWs](https://wiki.postgresql.org/wiki/Foreign_data_wrappers), you can create FDW to many other databases than postgres.
- Other SQL (MySQL, Oracle ...)
- NoSQL (MongoDB, Cassandra ...)
- Python (SQL_Alchemy...)
- File Wrapper (CSV ...)
- Big Data (BigQuery ...)
- Spreadsheets (GSheets ...)

Later on, watch this 1h talk [PostgresOpen 2019 Intro To FDW](https://www.youtube.com/watch?v=Swl0P7cP3-w) to dig deeper!

<br>

# 🏁 Finishing up

We hope this challenge illustrated the power of FDW using Docker compose to test new database architectures quickly without having to launch lots of extra postgres servers on your own hardware!

There are no tests for this challenge, but make sure to git add, commit, and push your code to Github so Kitt can track your progress!

<br>
