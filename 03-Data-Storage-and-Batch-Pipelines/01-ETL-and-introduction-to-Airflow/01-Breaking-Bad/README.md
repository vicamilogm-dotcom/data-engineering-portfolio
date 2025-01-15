# 🎯 Goal

Airflow is a common tool used by Data Engineers to **orchestrate processes**. These processes could be bash commands, python operations, sending emails, accessing API's, and many more.

The goal of this challenge is to setup an Airflow instance running in Docker Compose that will trigger a DAG every 5 minutes. The DAG will call an API, process the result, and append it to a CSV.

There is a few steps involved, so lets get into it! 🚀

<br>

# 1️⃣ Airflow Setup

First we'll have **Airflow running through docker-compose**.

To build the lightest version of Airflow you need at least three services:
- A **postgres database** to store Airflow *metadata* (e.g: what DAGs do I have to orchestrate, when was the last run,...)
- A **webserver** to display Airflow UI
- A **scheduler** to orchestrate and execute your DAGs (for example: start every 5 minutes...)

👉 Take a close look at the (un-finished) `docker-compose.yml` to get the big picture and see which service depends on which.

We also need some directories to store relevant relevant data and files used by Airflow:

- The `dags/` directory will contain your hand-coded Airflow logic
- The `data/` directory will store the output of your DAG (breaking-bad quotes, as CSV)
- The `logs/` directory will be used automatically by Airflow to sync data between its container and your local setup.

## 1.1. Setup the Dockerfile

You need to create the Airflow Dockerfile that will be used by your `webserver` and `scheduler` services. There are a lot of ways to build it, but we made our tests very strict to ensure that you all reach the same point to start the exercises of the day (you could have a setup that works but that does not pass the test).

The main requirements to respect will be to:
- Set the environment variable [`AIRFLOW_HOME`](https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html?highlight=airflow_home#envvar-AIRFLOW_HOME)
- Create a user for the Airflow metadata database (or skip if created) and launch the webserver
- Install `poetry` and the packages defined in the `pyproject.toml` and `poetry.lock`

You could use a pre-built Airflow image to start your Dockerfile but we will keep it as light as possible and use a python image to start. It will also give you more opportunities to learn Airflow setup commands 😉

1. Let's start by creating a `Dockerfile` and start from a `python:3.8.10-slim` image

1. Set the `DEBIAN_FRONTEND` argument to `noninteractive`

1. Set the `PYTHONUNBUFFERED` environment variable to `1`

1. Set the environment variable `AIRFLOW_HOME` to `/app/airflow`

1. Set the `WORKDIR` to `AIRFLOW_HOME`

    Now, it's time to take a look at the `scripts/entrypoint.sh` file that has been provided. It will be executed by the docker compose `webserver` service at startup and does the following:
        - Create an empty Airflow metadata database schema inside our "db" instance inside our "postgres" service
        - Create an Airflow user "Admin" password "admin" to access the webserver UI
        - [Start an Airflow `webserver` instance](https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html#webserver)

1. Copy the `scripts` directory inside the Docker image, then add a bash command to make `scripts/entrypoint.sh` executable

1. Finally, install Airflow and its dependencies via `poetry`:
    - Copy the `pyproject.toml` and the `poetry.lock` files to the Docker image
    - Add a bash command that runs three consecutive steps to upgrade pip (by skipping cache if it exists), install poetry, and finally install poetry packages without the dev packages

## 1.2. Setup the docker-compose.yml

As noted above, you will create a light docker-compose with the minimal requirements, but do not hesitate to take a look to the official docker-compose.yml of Airflow [here](https://github.com/apache/airflow/blob/main/docs/apache-airflow/howto/docker-compose/docker-compose.yaml).

### Postgres service

- You'll need to create a `.env` that contains your `POSTGRES_PASSWORD` that docker compose can read when you launch your services, but isn't hardcoded into your `docker-compose.yml`. Feel free to use the `.env.sample`
- You'll need 3 environment variables that define the name of the database, the user of the database, and the password the user will use to access the data:

```bash
- POSTGRES_DB=db
- POSTGRES_PASSWORD=$POSTGRES_PASSWORD
- POSTGRES_USER=airflow
```

- A volume to store PostgreSQL data into a local directory named database (`./database/:/var/lib/postgresql/data`)
- Map your localhost port `5433` to the postgres default container port `5432`

### Scheduler service
The [scheduler](https://airflow.apache.org/docs/apache-airflow/stable/concepts/scheduler.html) is responsible for:
- Orchestrate & schedule tasks
- Initiating the execution of DAGs
- Continuously monitor whatever is inside your `dag/` directory to fill-up airflow db with dag metadata.

To finalize setup of your scheduler, you therefore need to add the db connection string, and directory paths:

- Add some env variables (see [docs](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html)):

```bash
- AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2://... # ❓ YOUR TURN: Try to complete the connexion string
- AIRFLOW__CORE__EXECUTOR=LocalExecutor # 💡 In production you would use other values for distributed processing etc...
```

- Add 3 volumes to sync your local `dags`, `data` and `logs` directories to directories of the same name inside the Scheduler (they should be stored at the `/app/airflow` level on Airflow side)

### Webserver service

For your scheduler service you need to add:

- Five environment variables: the five that have already been defined for previous services
- The same 3 volumes as for the scheduler
- A mapping of your localhost `port 8080` to the container network `port 8080` (this will allow you to locally get the Airflow UI).

At that point, you should be able to run the following command (that will force rebuild the image of your Dockerfile and recreate your docker-compose):

```bash
docker compose up
```

If this doesn't work:
- Make sure your images are up to date (you should `docker-compose build` every time you update your dockerfile)
- Try to understand your error message
- If the error is about ports already being in use, check this [stackoverflow](https://stackoverflow.com/questions/38249434/docker-postgres-failed-to-bind-tcp-0-0-0-05432-address-already-in-use)
- Run these optional tests which check your Dockerfile & compose syntax, they may give you some hints

```bash
# You don't need to pass these tests if your docker compose runs correctly - they are too strict
pytest -v tests/test_dockerfile.py
pytest -v tests/test_docker_compose.py
```

Now, visit [localhost](http://localhost:8080/home). Have a look to the `scripts/entrypoint.sh` to find the login and password to use!

🧪 To test that the setup is working as intended, run:

```bash
make test_setup
```

If everything is green, don't forget to add, commit, and push your code before moving onto the next section!

## 1.3. Connect your local DBeaver app to the Airflow DB

Connect to the postgres instance running in docker compose via **DBeaver on your local machine**

<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W1D4/dbeaver_local.png" width=500>

You should see airflow tables storing all kind of metadata about your dags.
As you run jobs and update code in the local `dags` directory, this database will get updated by the scheduler.

<br>

# 2️⃣ Breaking Bad Quotes

Let's add our first Airflow DAG. It should run *every five minutes* and:
- Send a GET request to a Breaking Bad quotes API for a random Breaking Bad quote
- Save the received quote, but only if this quote has not already been saved

For the random quotes, you will use this [API](https://breaking-bad.lewagon.com/v1/quotes) - This is le wagon's mirror of this [educational API](https://breakingbadquotes.xyz/) to keep things stable.

For the saving system you will use a CSV file. Early in the dev cycle, you could use a CSV as a stand in database.

We split the instructions in three parts to help you create the DAG:
- DAG config
- Tasks
- Python functions

## 2.1. DAG Configuration 🔀

Open `dags/breaking_bad_quotes.py` - take the time to read through what is there and what you need to complete.

First, let's focus on creating the proper DAG configuration - no tasks or python functions for now.

You need to create a DAG with the following requirements:
- it should be named `breaking_bad_quotes`
- it should have a start_date equal to yesterday (be careful, Airflow is expecting a datetime object)
- it should have a description saying `A simple DAG to store breaking bad quotes`
- it should not catchup the missing runs
- it should be scheduled to run every 5 minutes
- it should not depend on previous runs (`default_args={"depends_on_past": False}`)

🧪 Once you think you have the DAG config, test with:

```bash
make test_dag_config
```

## 2.2. Tasks 🏋️‍♀️

Now it's time for you to create the tasks that your DAG will use.

We want the quotes to be saved in a specific CSV file. Your DAG needs a task to create the file, then it needs another task to request a quote and save it if it hasn't been seen before.

As we want your quotes to be saved in a specific CSV file, your DAG needs a task to create the file. Then, it needs another task to request a quote and save it if this is a new one.

You thus need two tasks:
1. A task_id `create_file_if_not_exist` that should trigger the python function of same name with the appropriate arguments.
2. task_id `get_quote_and_save_if_new` that should trigger the python function of same name, with the correct arguments.

👉 You should use use a [PythonOperator](https://airflow.apache.org/docs/apache-airflow/2.2.0/howto/operator/python.html). Note, that we explicitly gave you the link to PythonOperator for Airflow 2.2.0, we want you to use this style for now and not to confuse you with the newer style that is notably different to other Airflow operators.

👉 To help you, we have already added the related python functions signatures, but be careful:
**for this part, you don't have to fill the python functions but only to create the Airflow tasks that will call them.**

👉 We want your quotes to be saved to `/app/airflow/data/quotes.csv`.

👉 The second task should be triggered only once the first one succeeds.

🧪 Once you are confident with your code run:
```bash
make test_tasks_configs
```

Once you passed the tests, launch all your airflow service:
```bash
docker compose up
```

Finally, open [your localhost](http://localhost:8080/home) to see how your DAG looks.

You should see your two tasks. Turn the DAG on and see what happens! Both tasks should be green because your tasks call functions that do not do anything for now.

<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W1D4/first_dag.png" width=500>

## 2.3. Python Functions Instructions 🐍

To give you a starting point, we've provided the function signatures for five functions. It is now your turn to implement them in the correct combination and order. You should not have to create any other python functions. Remember that helper or internal functions (and variables) are usually prefixed with an underscore - `_`.

If you can't remember how the `requests` or `csv` packages work, check out the docs:
- Python [csv](https://docs.python.org/3.8/library/csv.html)
- Python [requests](https://pypi.org/project/requests/)

Do not hesitate to manually trigger the DAG to see what your code does.
No need to restart your `docker compose` when you change the DAG code, just refresh your browser.

If you need to restart from a clean base, you can empty your local `data/quotes.csv` file - it is synced with the one that Airflow uses.

🧪 If you think that you've completed all the functions, test with:
```bash
make test_python_functions
```

If everything is green, you should be able to trigger the DAG, see those tasks turning green, and have your `quotes.csv` being filled every few minutes 🎉

<br>

# 3️⃣ Airflow in a nutshell

The docker layer of complexity should not divert your from how Airflow works in a nutshell: important commands are located in `entrypoint.sh`.

```bash
airflow db upgrade # Create an airflow DB with correct schema and empty tables

airflow users create ... # Create a user for the webserver

airflow webserver # launch webserver
```

You could have run Airflow without docker with just: `pip install airflow`, but it's never how you'd use it in practice.

Let's see one more important airflow command.

### 💡 How to reset my airflow metadata DB entirely?

In case you want to replay your DAGs as if the were never run before, the best option is to reset your Airflow db entirely!

You can run `airflow db reset`, which will burn down and rebuild the metadata database

❓ **What command should you run to execute such command from inside your airflow webserver service?**

<details>
  <summary markdown='span'>💡 Hints</summary>
- You can either use `docker compose exec <your_command>` directly inside an already-running container
- Or if you stop all your containers first, try using `docker compose run -it ...`
</details>

👉 Give it a try! Check on your DBeaver - the `dag` table should be reset (make sure to refresh!), then after ~1 minute the scheduler will re-populate all your DAGs!

<details>
  <summary markdown='span'>🎁 Solution</summary>

```bash
docker compose exec webserver poetry run airflow db reset
# OR
docker compose down
docker compose run -it webserver poetry run airflow db reset
docker compose up
```
</details>

<br>

# 🏁 Finishing up

Congratulations, you now have orchestrated code running on a schedule!

🧪 To test the entire challenge, run:

```bash
make test
```

And don't forget to git add, commit, and push your code to Github to track your progress on Kitt!

Once you've committed all your code and `test_output.txt`, teardown the service to free up ports for the next challenge:

```bash
# To free-up your ports for next challenges
docker compose down
```

<br>
