# 🎯 Goal

In this challenge, you will focus on creating a more complex **ETL** pipeline. To allow you to focus on the Airflow side of things, we've provided the `Dockerfile` and `docker-compose.yml`. Make sure to read through them and understand how they're working.

We'll have:
For this pipeline, we'll have a few components and follow the *bronze, silver, gold* architecture:
- An API to call for data in JSON format
- A **data lake** (`data` directory) to store:
    - Raw JSON data in a **bronze** directory
    - Transformed JSON data in a **silver** directory
- A **data warehouse** (`postgres db`) to store transformed data in a structured manner.

The goal is to have a DAG running every day that will:
- **Extract** - Downloads a Chuck Norris' joke, using this [API](https://api.chucknorris.io), saving them as [JSON's](https://en.wikipedia.org/wiki/JSON) into the **bronze layer** of your **data lake**
- **Transform** - Translates it to Swedish, saving them again in the **silver layer** of your **data lake**
- **Load** - Inserts them it into your **data warehouse**

For sake of simplicity, in this challenge, the postgres "warehouse" will be the same postgres database used by Airflow as its metadata database, and is called `db`, as per docker-compose:
```bash
- POSTGRES_DB=db
- POSTGRES_USER=airflow
```

In this challenge we're using local components so you can focus on how the different parts of Airflow work. Later in the bootcamp we will see how Airflow connects to external sources like Google Cloud Storage as a data-lake and BigQuery as a warehouse instead.

<br>

# 1️⃣ Setup ⚙️

The `Dockerfile` and `docker-compose.yml` are similar to the previous challenge, with one exception: the `entrypoint.sh` now contains an additional line (to reference an additional script: `init_connections.sh`) to create a connection between the Airflow service and the warehouse.

```bash
airflow connections add 'postgres_connection' \
                    --conn-type postgres \
                    --conn-host "postgres" \
                    --conn-schema "$POSTGRES_DB" \
                    --conn-login "$POSTGRES_USER" \
                    --conn-password "$POSTGRES_PASSWORD" \
                    --conn-port "5432"
```

👉 Adding a connection is required to interact with the warehouse explicitly in our **load**  stage:

```python
PostgresOperator(
    sql=... # create warehouse table, insert translated jokes...
    postgres_conn_id='postgres_connection'
)
```

💡 We didn't need it in our previous challenge as we were not storing anything in a warehouse!

It will be helpful to create our bronze, and silver folder structure for our data now. Once the containers are spun up, Airflow will lock restrict permissions on the folders:

```bash
mkdir -p data/bronze
mkdir -p data/silver
```

Now, you just have to add your `POSTGRES_PASSWORD` in a new `.env` file, enable `direnv` then launch your containers:

```bash
docker compose up
```

You should be able to:
- Access the Airflow webserver on `localhost:8080`
- Access the Airflow db via DBeaver on port `localhost:5433`

<br>

# 2️⃣ DAG Instructions ↪

Like the previous challenge, we'll tackle this DAG in a similar way:
- DAG configuration - the `with DAG(...) as dag:` configuration
- Tasks - the definitions of all our tasks and the execution graph
- Python functions - the python functions called by our tasks

## 2.1. DAG Configuration

First, let's focus on creating the proper DAG configuration (no tasks or python functions needed for now).

You need to create a DAG with the following requirements:
- Should be named `local_etl`
- Should be scheduled to run every day, with a start date equal to five days ago (so we'll simulate 5 runs)
- Should have a description saying `A local etl`
- Should catchup the missing runs
- Should run only if the previous runs succeed

🧪 Once you are confident with your code, test with:

```bash
make test_dag_config
```

## 2.2. Tasks 🏋️

Now let's create the tasks that your DAG will use. This time you will create more tasks that will do less operations, providing greater granularity.

You need four tasks:

### 2.2.1. A `create_swedified_jokes_table` task_id
- As a [PostgresOperator](https://airflow.apache.org/docs/apache-airflow-providers-postgres/stable/_api/airflow/providers/postgres/operators/postgres/index.html#module-airflow.providers.postgres.operators.postgres) :
- That should create a table named `swedified_jokes` with 3 columns:
- `id` (serial primary)
- `joke` (varchar not null)
- `swedified_joke` (varchar not null)

### 2.2.2. `extract` task_id
- As a [BashOperator](https://airflow.apache.org/docs/apache-airflow/stable/howto/operator/bash.html):
- That uses [curl](https://en.wikipedia.org/wiki/CURL) to retrieve a random Chuck Norris' joke from [https://api.chucknorris.io](https://api.chucknorris.io).
- The joke should be saved to the **bronze** directory under the name `bronze/joke_{execution_date}.json` where `{execution_date}` corresponds to the execution date of the Airflow dag (for example: */app/airflow/data/bronze/joke_20220521.json*).

<details>
<summary markdown='span'>💡 Hint</summary>

Check out [airflow template variables](https://airflow.apache.org/docs/apache-airflow/stable/templates-ref.html) for a way to programmatically access Airflow variables at runtime. The values you need for this might already be provided
</details>

### 2.2.3. `transform` task_id
- As a [PythonOperator](https://airflow.apache.org/docs/apache-airflow/2.2.0/howto/operator/python.html)
- That should trigger the `transform` function with the proper arguments (don't fill the python function yet)
- The transformed joke should be saved to the **silver** directory under the name `silver/swedified_joke_{execution-date}.json` (for example: */app/airflow/data/silver/swedified_joke_20220521.json*).


### 2.2.4. `load` task_id
- As a `PythonOperator`
- That should trigger the `load` function with the proper arguments - don't fill python function just yet, we'll get to that in a bit.

### 2.2.5. Now, arrange your tasks
Time to put all the task together into an execution graph:
- The second task should be triggered only after the first one's success.
- The third task should be triggered only after the second one's success.
- The fourth task should be triggered only after the third one's success.

🧪 Once you are confident with your code, test with:

```bash
make test_tasks_configs
```

When all the tests are green, launch your Airflow instance and open [localhost](http://localhost:8080/home) to see how your DAG looks.

You should see your four tasks. Turn the DAG on and see what happens! It should be all green 🟢 as your tasks call functions that do not do anything for now.

## 2.3. Python Functions 🐍

To get you started, we have provided the signatures of 6 functions. Now it's your turn to implement them! Read the function docstrings carefully and make sure functions are returning the object types defined in the signature.

🧪 When you are ready to test your code, run:
```bash
make test_python_functions
```

Now you should be able to trigger the DAG, see green results and have your `swedified_jokes` table being filled! Check it out on DBeaver!

For some more tips, have a look at the next section!

<br>

# 3️⃣ Airflow Pro Tips 💡

## 3.1. Debugging in Airflow? 🐛

### Check logs on Airflow UI

The recommended starting point for debugging. Below, the second task of our first run has failed. And 4 other run are planned and running (they wait for the next 4 days to be finish)
You can click on "Log" to inspect logs

<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/airflow_failing.png">

### Check logs from your Terminal

You can access your logs from your terminal, but mixing logs of 3 services at once can be messy. Simply open 3 terminal, each with one of the commands:

```bash
docker compose logs -f postgres
docker compose logs -f scheduler
docker compose logs -f webserver
```

### Check logs from logs folder

You should be able to see the exact same information in your `logs` folder, which is precious to grep for "ERROR" lines etc...!

## 3.2. Reset Airflow DB

In case you want to replay your challenge history from scratch, you can reset your airflow metadata database as if the were never run before:

```bash
docker compose exec webserver poetry run airflow db reset
```

You can also `sudo rm -rf database` to obliterate it entirely, but that's not a great skill to master in real life 🫠

<br>

# 4️⃣ (Optional) Understand scheduler and webserver health checks

Have a look at the **healthchecks** in webserver and scheduler services of the `docker-compose.yml`. Understand how they work and what they are doing.

The endpoints are taken straight from Airflow's Health Status docs located at [this link](https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/logging-monitoring/check-health.html#).

Airflow has a built in *heartbeat* that updates and writes to the metadata database regularly. The **scheduler** healthcheck is just checking the most recent entry of that *heartbeat* to see if the scheduler is healthy.

Airflow has a `/health` endpoint to check the health of the **webserver**. We are simply pinging the API and if we receive a 200 http response, then we exit with status code `0`, telling Docker that the webserver container is healthy. A non 200 http response (4xx, 5xx) would exit with status code `1`, telling Docker that the webserver is unhealthy with the `|| exit 1` section of the healthcheck test.

<br>

# 5️⃣ (Optional) Understand tests in Airflow 🧪

It can be interesting to read our tests to learn how to write tests for your own DAGs!

👉 Have a look at your `makefile`, and let's focus on `test_dag_config`

- We don't want to test your code against your "production" database `db`.
- Therefore, every time you're running `make test_dag_config`, we're creating a local sqlite metadata db on which we will run your dags.
- How does it work?
  - We're changing AIRFLOW_HOME to a new temp folder.
  - Then run `airflow db init`, which will create a brand new airflow project which by default creates a sqlite metadata db with correct schema migrations.
- You can inspect the 3 files that were created inside `tests/temp`
  - `airflow.db` is the sqlite copy of your postgres metadata db. You can peer inside with VSCode SQLlite extension: you should see some swedified jokes inside it!
  - `webserver_config.py`
  - `airflow.cfg`
    - check line 185: your `sql_alchemy_conn` refers to that local sqlite!
    - compare it to that of your currently running app: `docker compose exec webserver poetry run airflow config get-value database sql_alchemy_conn`
- Open our `test_tasks_config.py`
  - line 18 we're using a DagBag to "parse" your dags from your local folder `./dags`. We'll then be able to tests your dag syntax without actually running anything (ex. line 39)
  - Then we also want to make fake "runs" of you dag against the temporary sqlite. For that, we first have to redirect the postgres connection by loading another `tests/scripts/init_connections.sh` from Makefile context. This allows us to override the Postgres hook on your DAG with a `SqliteHook` in our test (line 19). We can then use `hook.run(...)` on anything we want and launch your dag via `dag.create_dagrun(...)`. The process of replacing a variable with a different one of the same name at test time is called **mocking**.

<br>

# 🏁 Finishing up

Congratulations! You now have an orchestrated pipeline running in Airflow 🎉

🧪 Run `make test` to create a `test_output.txt`, then git add, commit, and push your code so Kitt can track your progress!

Once you're done with the challenge, don't forget to teardown your compose stack so it's not continuously running in the background and using system resources! To bring your stack down use:

```bash
docker compose down
```

Alternatively a great way to get an overview of all docker containers running, use the docker app in VS Code located on the left hand side.

<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/030102-vscode-docker-app.png">

From the list of running containers and compose stacks, you can:
- Right click on any individual container to attach a shell, start, or stop to the container.
- Right click a container group, like **02-local-etl** and `compose down`, `compose stop`, and more.

<br>
