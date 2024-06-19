# 🎯 Goals and Context

Welcome to the Database Fundamentals module!

SQL and database theory is foundational for a Data Engineer. We'll use it SQL for data management and retrieval, data transformations and in ELT pipelines, and integrating data into other tools, like BI tools for visualisation and reporting.

Database theory allows Data Engineers to design database schema for efficient data organisation, meaningful relationships between tables, optimised for performance, and match the business case and less technical end users, like Analysts.

Through the challenges for this unit we will:
- Spin up a postgres container to prepare our database
- Load some data into it
- Connect to with a SQL client on our local machine
- And get started with some warmup queries

Let's get to it! 🚀

<br>

# 1️⃣ Postgres in docker

We will start with creating a postgres docker container and use a [volume](https://docs.docker.com/storage/volumes/) so our database has persistence when we start and stop the container.

We will create a volume to keep the data for today:

```bash
docker volume create pgdata-0201
```

You will requires some credentials to connect to the postgres database, an convenient way to hold secrets is in a `.env` file. We've created a template you can use.

```bash
cp .env.sample .env
```

Edit the environment variables (if you wish), then run:

```bash
direnv reload
```

Launch the containerised postgres instance!

```bash
docker run -p 5410:5432 -e POSTGRES_USER=$POSTGRES_USER -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD -v pgdata-0201:/var/lib/postgresql/data postgres:15.4
```

We have a running postgres instance, but it has no databases or data inside it. Let's create a database for the data for today using the [pagila](https://github.com/devrimgunduz/pagila) example database.

You'll need to connect to `psql` inside postgres, inside the container. You can connect to the container with an interactive shell first then connect to `psql`, or connect directly to `psql`:

```bash
# Connect to the container
docker exec -it <YOUR_CONTAINER_NAME> /bin/bash

# Connect to psql
psql --user <YOUR_POSTGRES_USERNAME>
```

```bash
# Connect directly to psql
docker exec -it <YOUR_CONTAINER_NAME> psql --user <YOUR_POSTGRES_USERNAME>
```

<details>
<summary markdown='span'>❗ sql: error: connection to server on socket</summary>
If you get an error that looks similar to the following when you try to connect to `psql`:

```bash
psql: error: connection to server on socket "/var/run/postgresql/.s.PGSQL.5432"
failed: FATAL: role "<YOUR_POSTGRES_USERNAME> does not exist"
```

You might not have reloaded your `.env` after changing the `POSTGRES_USER` or `POSTGRES_PASSWORD`

The easiest fix is to do a complete teardown:
- Stop your running postgres container
- Remove your postgres container: `docker rm <YOUR_CONTAINER_NAME>`
- Delete the volume that is holding your persistent data. When the postgres container was first run, postgres has an initialisationit that created a super-user with the values in your `.env`:
    ```bash
    # List volumes
    docker volume ls

    # remove volume
    docker volume rm <VOLUME_NAME>
    ```
- Make sure your `.env` values are loaded: `direnv reload`
- Recreate the volume and relaunch the container.
</details>

In the `psql` shell, you can create the pagila database:
```sql
CREATE DATABASE pagila;
```

And it should now be created! 🎉

There are some other useful [meta commands](https://www.postgresql.org/docs/current/app-psql.html) you can use in `psql` to investigate different databases and tables.

```bash
# List all databases
\l

# Connect to a database - e.g. connect to pagila
\c pagila

# List the tables of the current database
\d

# Exit psql
\q
```

Have a play around in the postgres instance and see what you can find!

<br>

# 2️⃣ Load data into database

It's time to load the data into our `pagila` database. Navigate back to your VM's terminal then execute the following commands to load data into the database.

Then, execute the following two commands back in the terminal to get the data into the database. Read the commands carefully and change the relevant parts.

```bash
# Load the schema - defines tables, dtypes, nullable
curl -L https://raw.githubusercontent.com/devrimgunduz/pagila/e1e5a855c46176bc0e17b7e8dea2f61e555fb378/pagila-schema.sql | docker exec -i <YOUR_CONTAINER_NAME> psql --username=$POSTGRES_USER --dbname=pagila -a -f-
```

```bash
# load the data into the tables
curl -L https://raw.githubusercontent.com/devrimgunduz/pagila/e1e5a855c46176bc0e17b7e8dea2f61e555fb378/pagila-data.sql | docker exec -i <YOUR_CONTAINER_NAME> psql --username=$POSTGRES_USER --dbname=pagila -a -f-
```

Lets break down what is happening here:
- The `curl` command is downloading the relevant data from a remote github repository
- The `|` is piping the `stdout` from the `curl` command to the next command
- `docker exec -i <YOUR_CONTAINER_NAME>` is interactively acting with your container, keeping `stdin` open
- `psql --username=$POSTGRES_USER --dbname=pagila -a -f-` is:
  - Opening `psql` as your `$POSTGRES_USER` to the `pagila` database
  - `-a` is echoing all input lines before they are processed, useful for debugging
  - `-f` is specifying the file to execute SQL commands from
  - The single `-` at the end of `-f-` tells `psql` to read SQL commands from `stdin`, allowing us to pipe SQL commands into `psql`

While you are could technically start building your queries now, `psql` is a bit clunky to work with. Let's connect our database to a SQL client.

<br>

# 3️⃣ Connect your containerised postgres instance to DBeaver

We have a database with data up and running, but interacting via `psql` isn't the best developer experience. Let's connect our container to DBeaver, a SQL client that will be easier to write our queries in.

## 3.1. Port forwarding

We'll need to forward some ports to get a connection from DBeaver on our local client to the database inside a container, running on our virtual machine. It's easy to lose track of what ports are moving what data.

By default postgres runs on port 5432, but we *already* have a postgres instance running on our VM (not in a container) that is using port 5432. You can test this yourself by running `service postgresql status` in your VM terminal.

In the `docker run ...` command to launch the postgres container we mapped port 5432 *inside* the container to port 5410 *outside* the container. You can then forward this port on your VM to your local computer.

<p><img src="https://wagon-public-assets.s3.eu-west-3.amazonaws.com/mxu52b1j4p48yn68encsm9c2qp67" width="800"></p>

## 3.2. Connecting via DBeaver

With the port forwarded to our local computer, we've opened up the channel for data to move through. We'll need to make a new connection to our database via DBeaver so we can easily interact with it.

Open DBeaver and click the **New Connection** button in the top left, then select `postgres`

<p><img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W0D3/dbeaver-new-conn.png" width="800"></p>


Fill out the `postgres` connection page. Key inputs are in the red boxes:
- Database: pagila
- Port: the port you forwarded
- Username: `POSTGRES_USER` in your `.env`
- Password: `POSTGRES_PASSWORD` in your `.env`

<p><img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W0D3/postgres-connection.png" width="800"></p>

It is worth using the **test connection** button on the database connection wizard to make sure everything is working as intended.

Once you have an active connection, create a SQL script and run a test query against the database!

<p><img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W0D3/connected-dbeaver.png" width="800"></p>

You should now be ready for a few warm up queries!

<br>

# 4️⃣ Warm up queries

Investigate the schema in DBeaver to familiarize yourself with the data. Once you're ready, let's do a few warm up queries.

Feel free to iterate towards your solution using DBeaver. To run the unit tests, copy and paste the query into the relevant SQL file in the challenge directory on your VM.

## 4.1. Actors

❓ Generate a list of actors who have acted in more than five films.

- Your output should have two columns: the `actor_id` and the `total_films` in which they have appeared. - Order the result by the number of films in descending order.
- Only include actors who have acted in more than five films in your result.

🧪 Once you are happy, copy your query into `actor_query.sql` and run:

```bash
make test
```

## 4.2. Rentals

❓ Produce a query that lists each film, its category, and the number of times it's been rented.

- Your output should have three columns: `title` (of the film), `category_name` (name of the category), and `rental_count` (number of times the film has been rented).
- Make sure to include films that have never been rented.
- Arrange the results by the `rental_count` in descending order so that the most rented film appears first.

🧪 Once you are happy with your query, copy it into `rentals_query.sql` and run:

```bash
make test
```

## 4.3. Monthly revenue

❓ Calculate the monthly revenue for the year 2022

- Your output should consist of two columns: `month` (represented as a number from 1 to 12) and `monthly_revenue` (sum of all payment amounts for that month).
- Order the result by month in ascending order.

🧪 Once you are happy with your query, copy it into `monthly_revenue_query.sql` and run:

```bash
make test
```

<br>

# 🏁 Finish

We've set up our database and warmed up with a few queries, you are ready to move on and continue to work with this database and deal with some more advanced SQL.

🧪 Run `make test`, commit, and push to github so Kitt can track your progress!

<br>
