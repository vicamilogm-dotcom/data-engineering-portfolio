# 🎯 Introduction

This is a short tutorial to let you use Airflow to orchestrate your dbt jobs.

For that purpose, we will *mount* a live copy of our DBT models *inside* the airflow instances.

More precisely, we will have 3 containers running:
- a postgres db storing airflow metadata
- 2 Airflow services (scheduler + webserver), in which we will **mount** our DBT folders.

The *actual datasets and models* will then be saved in Big Query.

# 1️⃣ Setup

We already created a dbt project (`dbt_lewagon`) for you that contains the basic models coming from `dbt init`, which will be enough to test your setup.

## Dockerfile
First, let's note that we already added `dbt-core` and `dbt-bigquery` to your `pyproject.toml` (that Airflow will use).

Then, there are several environment variables for Airflow to know in which folders to look up when running `dbt` commands. Open your `Dockerfile` and add the following lines after `ENV AIRFLOW_HOME=/app/airflow`:

```
ENV DBT_DIR=$AIRFLOW_HOME/dbt_lewagon
ENV DBT_TARGET_DIR=$DBT_DIR/target
ENV DBT_PROFILES_DIR=$DBT_DIR
ENV DBT_VERSION=1.1.1
```

You may have noticed that you set `$DBT_PROFILES` to `/app/airflow/dbt_lewagon`, which means that you will have to create a `profiles.yml` in this folder (don't do it for now, this will be asked below).

Once you are confident with what you've done, run the tests:

```bash
make test_dockerfile
```

## docker-compose.yml

You should just have to mount two volumes in your `airflow scheduler` to sync:
- your local `dbt_lewagon` folder to your docker container
- your local `.gcp_keys` folder to your docker container (you will probably have to set the entire path to your `.gcp_keys`, like `/Users/username/.gcp_keys:/app/airflow/.gcp_keys`)

Once you are confident with what you've done, run the tests:

```bash
make test_docker_compose
```

Before moving to the next part, create and fill your `.env` file as usual with what's needed.

## Setup files

In order to run dbt with its own configuration, Airflow needs a `profiles.yml` in the `dbt_lewagon` folder:
- it should contain a `dbt_lewagon` profile
- with a `dev` output like that:
    ```yml
    dataset: dbt_write_your_name_here_day2
    job_execution_timeout_seconds: 300
    job_retries: 1
    location: US
    method: service-account
    priority: interactive
    project: # Your google cloud project name
    threads: 1
    type: bigquery
    keyfile: /app/airflow/.gcp_keys/the_name_of_your_keyfile.json
    ```
- and `target` should points to `dev`


Once you are confident with what you've done, run the tests:

```bash
make test_profiles_yml
```

# 2️⃣ Basic DAG: dbt run ➡ dbt test

The goal of this exercise is to have dbt installed on Airflow and to have a DAG with two tasks that trigger `dbt run` and `dbt test`.


## `dags/basic/dbt_basic.py`

❓ Open the `dbt_basics.py` file and add 2 tasks inside the DAG:

1. `dbt_run` BashOperator that runs dbt models, be careful, [you will have to specify the dbt_dir folder](https://docs.getdbt.com/dbt-cli/configure-your-profile#advanced-customizing-a-profile-directory)
2. `dbt_test` BashOperator that run dbt tests, be careful, [you will have to specify the dbt_dir folder](https://docs.getdbt.com/dbt-cli/configure-your-profile#advanced-customizing-a-profile-directory)

## Run it!
Run your DAG by unpausing it from the UI (or from the command line like a boss 😎, with `airflow dags unpause <dag_id>` but with in the correct docker context ;)

Then check that your setup worked, by opening your [BigQuery console](https://console.cloud.google.com/bigquery) and verify that you have a new dataset named `dbt_your_name_name_day2` that contains your two models.

When running this DAG, you should have the `dbt_test` failing, but this is normal, remember that this is how the `dbt_init` was built. However, make sure that the error you have is the expected one:

```markdown
Failure in test not_null_my_first_dbt_model_id (models/example/schema.yml)
Got 1 result, configured to fail if != 0
```

Once you are confident with what you've done, run the tests:

```bash
make test_dag_and_task_basic
```

>💡 This setup would scale with any other dbt_projects: Just replace the `dbt_lewagon` folder with the project that you've done in the previous day, make sure that it runs properly and go to BigQuery to check that your models have been created :)

🧪 Run all tests at once and git add, commit and your `test_output.txt`!

```
make test
```

# 3️⃣ Advanced DAG: one task per DBT model (Optional)

## Setup

In previous section, we integrated dbt to Airflow at a **project level**: One task was running "all dbt models", while the second was just about testing them. You could have done the same with a simple github action that would trigger `dbt test` at each pull-request.

In this exercise, your will integrate it at a **model level**. This means that your goal will be to have **a DAG containing one task per model**.

👉 First, let's change our target bigquery database by **updating your dbt/profile.yml**:
```
dataset: dbt_..._day2_advanced
```

## The DAG

**💡 How will we proceed?**

Here, we only have 2 dbt models, but imagine we had hundreds of them: We don't want to write hundred-times airflow tasks manually!

Hopefully, DBT generates a **[`manifest.json`](https://docs.getdbt.com/reference/artifacts/manifest-json)** file that we can parse!
- Have a look at `dbt_lewagon/manifest.json`: this file contains all models and their dependencies.
- PS: In reality, this manifest is much longer and is located at `manifest.json` in dbt_lewagon/target/manifest. We have trimmed the JSON for you to keep only the needed parts and make it more readable :)

👉 You won't manually declare your task but you will **generate them iteratively by using python functions**. To help you understand this new concept called meta-programming, we already added for you the functions calls such that you just have to code the functions themselves.

❓ **Open the `dbt_advanced.py` file and check the DAG inside. Your goal is to fill the python function accordingly.** Here is a summary of the flow:

- the `load_manifest` function will be called first and will be given the `manifest.json` path that it will load as a `dict` and return
- the returned `dict` will be given to the `create_tasks` function that will build a dict containing the `nodes` of the `manifest.json` as keys and their corresponding BashOperators as values
- these BashOperators will be built by the `make_dbt_task` function that will be called by the `create_tasks` function for each node by giving the proper dbt verb (`run` or `test`)
- the `create_dags_dependencies` function will reuse this `dict` to create the Airflow tasks. To order them properly, this function will have to manipulate the `depends_on` field of the `manifest.json`

🏋🏽‍♂️ This exercise is quite challenging to implement, so do not hesitate to check with a teacher that you have properly understood the requirements before starting.

At the end, you should have a DAG that looks like this
<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W2D3/dbt_dag.png">.

As always, once your confident with what you have done, try to run it and see if it worked on BigQuery!

Then, run the following command:

```
make test_dag_and_task_advanced
```

Again, once done, do not hesitate to make it work with your own models.

# 🏁 Congratulation

🧪 Run all tests at once and git add, commit and your test_output.txt!
```
make test
```
