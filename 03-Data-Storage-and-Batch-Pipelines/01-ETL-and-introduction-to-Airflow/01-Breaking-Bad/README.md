🎯 The goal of this challenge is to setup a local instance of Airflow that will trigger a DAG every 5 minute that will call an API, process its result, and append it to a CSV.

# 1️⃣ Airflow Setup


🎯 Let's have **Airflow running through docker-compose**.

To build the lightest version of Airflow you need at least three services:
- a **postgres database** to store Airflow *metadata* (e.g: what dags do I have to orchestrate, when was the last run,...)
- a **webserver** to display Airflow UI
- a **scheduler** to orchestrate your future DAGs (like: start every 5 minutes....)

👉 Take a close look at the (un-finished) `docker-compose.yml` get the big picture and see how which service depends on which.

We also need some folder to store data and instructions:

1. The `dags` folder will contain your hand-coded Airflow logic
2. The `data` folder will store the output of your DAG (breaking-bad quotes, as CSV)
3. The `logs` folder will be used automatically by Airflow to sync data between its container and your local setup.

## 1.1) Setup the Dockerfile

You need to create the Airflow Dockerfile that will be used by your `webserver` and `scheduler` services. There are a lot of ways to build it, but we made our tests very strict to ensure that you all reach the same point to start the exercises of the day (that's why you could have a setup that works but that does not pass the test).

The main requirements to respect will be to:
- set the environment variable [`AIRFLOW_HOME`](https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html?highlight=airflow_home#envvar-AIRFLOW_HOME)
- install the `PostgreSQL` client
- install `poetry` and its content

You could use a pre-built Airflow image to start our Dockerfile but we will keep it as light as possible and use a python image to start. Besides, it will better teach you airflow setup commands.

1️⃣ Let's start by creating a `Dockerfile` and make it start from a `python:3.8.10-slim` image

2️⃣ Set the `DEBIAN_FRONTEND` argument to `noninteractive`

3️⃣ Set the `PYTHONUNBUFFERED` environment variable to `1`

4️⃣ Set the environment variable `AIRFLOW_HOME` to `/app/airflow`

5️⃣ Move your `WORKDIR` on it

Now, it's time for you to take a look at the `scripts/entrypoint.sh` file that we have created for you. It will be executed by docker-compose `webserver` at startup and does the following:
- Create an empty Airflow metadata database schema inside our "db" instance inside our "postgres" service
- Create an Airflow user "Admin" password "admin" to access the webserver UI
- [start an Airflow `webserver` instance](https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html#webserver)

6️⃣ Copy the `scripts` folder inside the Docker image, then add bash command to make `scripts/entrypoint.sh` runnable.

7️⃣ Finally, you will have to install airflow via `poetry`:
- Copy the `pyproject.toml` and the `poetry.lock` files to the Docker image
- Add a bash command that run three consecutive steps to upgrade pip (by skipping cache if it exists), install poetry and finally install poetry packages without the dev packages

## 1.2) Setup the docker-compose.yml

As explained above, you will create a light docker-compose with the minimal requirements, but do not hesitate to take a look to the official docker-compose.yml of Airflow [here](https://github.com/apache/airflow/blob/main/docs/apache-airflow/howto/docker-compose/docker-compose.yaml).

### Postgres service

- You'll need 3 environment variables, and to create an `.env` file to set your password to the value of your choice.

```bash
- POSTGRES_DB=db
- POSTGRES_PASSWORD=$POSTGRES_PASSWORD
- POSTGRES_USER=airflow
```

- A volume to store PostgreSQL data into a local folder named database (`./database/:/var/lib/postgresql/data`)
- Map your localhost port 5433 to the postgres default container port 5432

### Scheduler service
The [scheduler](https://airflow.apache.org/docs/apache-airflow/stable/concepts/scheduler.html) is responsible for:
- Orchestrate & schedule tasks
- Continuously monitor whatever is inside your "dag" folder to fill-up airflow db with dag metadata.

To finalize setup of your scheduler, you therefore need to add the db connection string, and folder paths:

- Add some env variable (see [docs](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html)):
    ```bash
    - AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2://... # ❓ YOUR TURN: Try to complete the connexion string
    - AIRFLOW__CORE__EXECUTOR=LocalExecutor # 💡 In production you would use other values for distributed processing etc...
    ```

- Add 3 volumes to sync your `dags`, `data` and `logs` folders with Airflow ones (they should be stored at the `/app/airflow` level on Airflow side)

### Webserver service

For your scheduler service, you need to add:

- 5 environment variables: the five that you already added in the previous services
- the same 3 volumes as for the scheduler
- a mapping of your localhost `port 8080` to the container network `port 8080` (this will allow you to locally get the Airflow UI).

At that point, you should be able to run the following command (that will force rebuild the image of your Dockerfile and recreate your docker-compose):

```bash
docker compose up
```

If this doesn't work:
- Make sure your images are up to date (you should `docker-compose build` every time you update your dockerfile)
- Try to understand your error message first
- If it's about ports being already in used, check this [stackoverflow](https://stackoverflow.com/questions/38249434/docker-postgres-failed-to-bind-tcp-0-0-0-05432-address-already-in-use)
- Run these optional tests which check your Dockerfile & compose syntax, they may give you some hints

```bash
# You don't need to pass these tests if your docker compose runs correctly - they are too strict
pytest -v tests/test_dockerfile.py
pytest -v tests/test_docker_compose.py
```

Now, visit [localhost](http://localhost:8080/home). Have a look to the `scripts/entrypoint.sh` to find the login and password to use!

**🧪 Run `make test_setup`**

### 1.3) Connect your local DBeaver app to the airflow db 💽

Connect to your postgres via **DBeaver on your local machine**, after allowing for port-forwarding 5433

<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W1D4/dbeaver_local.png" width=500>

You should see all many airflow tables storing all kind of metadata about your dags.
As you run jobs and update your code in folder `dags`, this database will gets updated by the scheduler.

<br>

# 2️⃣ Breaking Bad Quotes

🎯 Let's add our first Airflow DAG. It should run *every five minutes* and:
- request a generator of "Breaking Bad" 🎥 quotes
- save the received quote (only if this quote has not been saved yet)

For the quotes generator, you will use this [API](https://breaking-bad.lewagon.com/v1/quotes) - This is le wagon's mirror of this [educational API](https://breakingbadquotes.xyz/) to keep things stable.

For the saving system, you will use a CSV file. [This kind of files could be considered as databases in development environments](https://en.wikipedia.org/wiki/Comma-separated_values).

We split the instructions in three parts to help you create the needed DAG.

## a) DAG Instructions 🔀

Take time to open the `dags/breaking_bad_quote.py` and discover the functions' signatures that we have added to help you.

First, let's focus on creating the proper DAG configuration (no tasks or python functions needed for now).

You need to create a DAG with the following requirements:
- it should be named `breaking_bad_quotes`
- it should have a start_date equal to yesterday (be careful, Airflow is expecting a datetime object)
- it should have a description saying `A simple DAG to store breaking bad quotes`
- it should not catchup the missing runs
- it should be scheduled to run every 5 minutes
- it should not depend on previous runs (`default_args={"depends_on_past": False}`)

Once, you are confident with your code run:
```bash
make test_dag_config
```

## b) Tasks Instructions 🏋️‍♀️

Then, you have to create the tasks that your DAG will use.

As we want your quotes to be saved in a specific CSV file, your DAG needs a task to create the file. Then, it needs another task to request a quote and save it if this is a new one.

You thus need two tasks:
1. a task_id `create_file_if_not_exist` that should trigger the python function of same name, with the proper arguments
2. task_id `get_quote_and_save_if_new` that should trigger the python function of same name, with proper arguments too.

👉 You should use use a [PythonOperator](https://airflow.apache.org/docs/apache-airflow/2.2.0/howto/operator/python.html). Note, that we explicitly gave you the link to PythonOperator for Airflow 2.2.0 even if we use the 2.3.0, as we want you to use this style for now and not to confuse you with the new style that is quite different to the other Airflow operators.

👉 To help you, we have already added the related python functions signatures, but be careful:
**for this part, you don't have to fill the python functions but only to create the Airflow tasks that will call them.**

👉 We want your quotes to be saved to `/app/airflow/data/quotes.csv`.

👉 The second task should be triggered only once the first one succeeds.

🧪 Once you are confident with your code run:
```bash
make test_tasks_configs
```

Once you passed the tests, start your docker-compose:
```bash
docker compose up
```

Finally, open [your localhost](http://localhost:8080/home) to see how your DAG looks.

You should see your two tasks. Turn the dag on and see what happens! It should be all green as your tasks called functions that do not do anything for now.

<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W1D4/first_dag.png" width=500>

## Python Functions Instructions 🐍

To help you, we have already added the signature of 5 functions. This is now your turn to implement them in the current order. You should not have to create any other python functions but will probably have to read the followings documentations:
- [https://docs.python.org/3.8/library/csv.html](https://docs.python.org/3.8/library/csv.html)
- [https://fr.python-requests.org/en/latest/](https://pypi.org/project/requests/)

Do not hesitate to manually trigger the DAG to see what your code does.
No need to restart your `docker-compose` when you change the DAG code, just refresh your browser.

If you need to restart from a clean base, you can empty your local `data/quotes.csv` file (it is synced with the one that Airflow uses).

Once you are confident with your code run:
```bash
make test_python_functions
```

🎉 Now, you should be able to trigger the DAG, see green results and have your `quotes.csv` being filled every few minutes ;)

## Final words on Airflow

The docker layer of complexity should not divert your from how airflow work in a nutshell: important commands are located in `entrypoint.sh`.

```bash
airflow db upgrade # Create an airflow DB with correct schema and empty tables

airflow users create ... # Create a user for the webserver

airflow webserver # launch webserver
```

You could have run it all without docker after a `pip install airflow`, but it's never how you'd use it in practice.

Let's see one more important airflow command...

### 💡 How to reset my airflow metadata DB entirely?
In case you want to replay your DAGs as if the were never run before, the best option is to reset your airflow db entirely!

You want to run `airflow db reset`, which will burn down and rebuild the metadata database

❓ **What command should you run to execute such command from inside your airflow webserver service**?

👉 Give it a try ! Check on your DBEAVER, the `dag` table should be reset (click "refresh"), then after 1 min the scheduler will re-populate all your DAGS!

<details>
  <summary markdown='span'>💡 Hints</summary>
- You can either use `docker compose exec <your command>` directly inside your already-running container
- Or you stop all your running containers first, then try using `docker compose run -it ....`
</details>

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


## 🏁 Congratulation! `make test` to create test_output.txt, then add, commit and push your code so we can track your progress!

```bash
docker compose down # To free-up your ports for next challenges
```
