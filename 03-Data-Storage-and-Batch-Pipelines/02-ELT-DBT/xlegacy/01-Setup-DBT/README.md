# ❗ Legacy Challenge ❗

This is a legacy challenge and has been archived as is.

It has been left available if you want to practice, but will not contribute towards your mandatory challenge completion percentage as part of the Le Wagon Data Engineering Bootcamp.

If you want to do these challenges, here are a few notes:
- The `pyproject.toml` has been renamed to `pyproject.toml.bak`.
    - This was done so that a virtual environment for this challenge was not installed when your ran `make install` on Setup Day, reducing disk usage.
    - If you want to install the poetry virtual environment, rename the `pyproject.toml.bak` to `pyproject.toml` and run: `poetry install`
    - You may need change the path of the package: `lewagonde` in the `pyproject.toml`. `lewagonde` contains helper functions for testing.
- Consider creating a new dbt profile for these challenges. Such as: `dbt_hackernews`
- This challenge was created using Python 3.8. If you drop in a `pyproject.toml` from any of the greenweez challenges, they *should* work, but we make no guarantees.

# 🎯 Goals

DBT (Data Build Tool) is crucial in data engineering because it enables data teams to transform raw data into clean, structured datasets using plain SQL. It simplifies the process of building and maintaining data transformation pipelines by allowing engineers to write modular, reusable SQL code. DBT also facilitates version control, testing, and documentation, making data workflows more reliable and scalable. By integrating well with modern data warehouses, DBT streamlines data modelling and ensures data quality, helping teams deliver consistent and accurate insights.

In this challenge we'll get DBT setup and start with the build in example before moving onto the next, more substantial challenge.

There are 5 steps in this setup:
1. Setup Big Query
1. Install DBT
1. Build a DBT project (folder structure + config file)
1. Setup the connection configuration with BigQuery (profile file)
1. Run your first DBT models, which will generate *tables* and *views* in BigQuery

<br>

# 1️⃣ Setup Big Query

BigQuery enables you to query data stored in different locations / projects. In this challenge, we'll be interacting with 2 projects:
- The project where the source data is stored. It's a project made public by Google to enable Data Scientists to play around with data. The project is called `bigquery-public-data`, and the name of the dataset is `hacker_news`
- Your own project, that you created during the Data Engineering Setup.

Let's pin those 2 in the BigQuery interface.

1. Go to the BigQuery interface [here](https://console.cloud.google.com/bigquery)

1. Star the `bigquery-public-data` project so you can more easily interact with it: Click on **ADD DATA > Star a project by name**, type: `bigquery-public-data`. Hit **STAR**

1. Do the same thing with your own project: in the example / screenshot below, the "personal" project is called `ingka-data-engineering-dev`

1. Your BigQuery interface should now look like this (except that instead of `ingka-data-engineering-dev`, it will be your project name):

<img src='https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W2D1/bigquery_interface_final.png' size=200>

<br>

# 2️⃣ Install DBT

- There are multiple versions of DBT, which vary depending on the database system you're interacting with. In our case, we're using BigQuery, so we'll also be installing `dbt-bigquery`. Make sure it's part of the packages included in `pyproject.toml`, and run `poetry install` in the `01-Setup-DBT` folder to install it.
- Make sure DBT is installed by executing `dbt --version` in your terminal.

<details>
  <summary markdown='span'>💡 How to check DBT version with poetry</summary>

```bash
poetry show dbt-core
# OR
poetry show | grep dbt
```

</details>

<br>

# 3️⃣ Initialize the DBT project

## 3.1. Initialize `dbt_lewagon` directory

DBT works by creating a DBT project directory inside your project. This directory is where all our models, SQL files, and (most) configuration files will be.

- In your terminal, go at current-challenge root. This is where we'll create the DBT project.
- Once there, you need to init (create the folder structure) of the DBT project - we'll call it `dbt_lewagon`.
- In command lines, run `dbt init`. When prompted:
  - _Enter a name for your project (letters, digits, underscore):_ Enter `dbt_lewagon`. If prompted: _The profile dbt_lewagon already exists in ~/.dbt/profiles.yml. Continue and overwrite it?_ Hit `N`.
  - _Which database would you like to use? Enter a number:_ Enter `1` (for `bigquery`)
  - _Desired authentication method option (enter a number):_ Enter `2` (for `service_account`)
  - _keyfile (/path/to/bigquery/keyfile.json):_ Enter the absolute path of where you stored your BigQuery service account key (that you created during the Data Engineering setup, [here](https://github.com/lewagon/data-engineering-setup/blob/main/macOS.md)), including the file name and its extension. Meaning it should look something like this:  `/home/username/code/.gcp_keys/le-wagon-de-bootcamp.json` (If you spell it wrong, you'll be able to modify it later).
  - _project (GCP project id)_: Enter your Google Cloud project ID (that you created during the Data Engineering setup, [here](https://github.com/lewagon/data-engineering-setup/blob/main/macOS.md))
  - _dataset (the name of your dbt dataset):_ Please be cautious here. Call it `dbt_{firstletteroffirstname}{last_name}_day1`. If your name is Barack Obama your dataset should be `dbt_bobama_day1`.
  - _threads (1 or more):_ Enter `1`
  - _job_execution_timeout_seconds [300]:_ Enter `300`
  - _Desired location option (enter a number):_ Enter `1` for `US`. This is important! The dataset we'll be exploring is located in the US - it facilitates things if you set up a "receiving" dataset that's also in the US.

This should have done 2 things:
- It generated all the tree structure needed for the DBT project under the `dbt_lewagon` folder
- It should have created a `profiles.yml` file at the following location: `~/.dbt/profiles.yml`

## 3.2. Verify the setup of `profiles.yml`

_High level info (no action item): the section relates to the DBT profile. 1 DBT project maps to 1 DBT profile, which generally maps to 1 company. Typically as a Le Wagon teacher, in my `profiles.yml` I have 2 profiles: 1 for LeWagon, 1 for the company I work at. The Le Wagon profile can write to several "targets": 1 target corresponds to a location where the profile can insert some data. Hence, each target is associated to a Data Warehouse system (BigQuery, Redshift etc), credentials with certain accesses, a location for the target (where the data will be inserted / in which dataset? etc)_

_For more information about the DBT profile, you can read this documentation:_
- _[`profiles.yml`](https://docs.getdbt.com/reference/profiles.yml)_
- _[BigQuery profile](https://docs.getdbt.com/reference/warehouse-profiles/bigquery-profile)_

Let's check that the `profiles.yml` file is configured correctly:
- Your DBT profile should be stored in a folder at your root called `.dbt`. Open it by running: `code ~/.dbt/profiles.yml`. You should be able to see all the configuration you've set when creating the DBT project.
- Run `make test` to make sure the setup of your profile is correct. (The `test_dbt_profile` tests should all be green). Watch out with the levels of indentation in your `profiles.yml` file
- Push to git.

### 3.2.1. Verify `dbt_project.yml` file

_No action item in this section - we're just providing context._

- Open the `dbt_lewagon` folder, and open the `dbt_project.yml` file in this folder:
  - Verify that the project name is correct: `name: 'dbt_lewagon'`
  - Verify that the profile name is correct: `profile: 'dbt_lewagon'`
  - At the bottom of the file, change, make sure the `models` parameter refers to your project name:
  ```yml
  models:
  dbt_lewagon:
    # Config indicated by + and applies to all files under models/example/
    example:
      +materialized: view
  ```

What is this? We're defining the default behaviour of our models. Models created by DBT will be created as `views` in our data warehouse unless specified otherwise. Keep reading to see how!

### 3.2.2. Verify initial tree structure of the DBT project

_No action item in this section - we're just providing context._

First, make sure that in the `models` folder, there should be two files:
- `/example/my_first_dbt_model.sql`
- `/example/my_second_dbt_model.sql`
- Check how the configuration of those models is built:
    - `my_first_dbt_model.sql` is generating some dummy `source` data, through a CTE, and is then storing this result in a `table`, called `my_first_dbt_model`.
        - The block at the top of the model defines the output should be a table, overriding the default materialization.
        - The table is called `my_first_dbt_model` - it uses the name of the file
    - `my_second_dbt_model.sql` is references to `my_first_dbt_model` model.
        - The materialization is not specified so it will be stored as the default materialization defined in the `dbt_project.yml` - a view

Let's explore the `/models/example/schema.yml` file. In there you can find:
- The list of models in the folder
- A high level description of each model
- For each column of each model, the ability to document:
    - its description
    - its constraints (unicity, the field not being null etc).

<br>

# 4️⃣ Enhance DBT project tree

❗ **From now on, all command lines assume you're executing them from your `dbt_lewagon` directory** ❗

### 4.1. Organising DBT Models

Let's organize the project better. We'll be working with three layers, similar to a bronze, silver, gold architecture:
- the `source` data
- the `staging` data - which is cleaner version of the `source` data
- the `mart` data - which contains clean metrics business stakeholders can report on.

Let's make sure the `.sql` file corresponding to each layer is in a folder that corresponds to what they're supposed to do: `cd` to the `dbt_lewagon` directory. From there, execute the following command:

```bash
mkdir models/source;
mkdir models/staging;
mkdir models/mart;
```

### 4.2. Reorganise macros

Macros are pieces of reusable code which work like functions in Python. They take inputs, give an output, and can be used throughout different models in your project. To better organise our `macros` based on function, let's restructure the `macros` folder. From the `dbt_lewagon` directory execute the following command:

```bash
mkdir macros/meta;
mkdir macros/models;
```

- `meta` macros used for project / architecture related functions
- `models` macros used for functions automating some parts of specific models

We built the above structure (`mart` and `staging` folders) for a specific reason, when we organise our models in directories, our tables/views in BigQuery will be prefixed to make them more identifiable. We want `.sql` models:
- in our `staging` directory to create schemas in BigQuery that are prefixed with `stg_`
- In our `mart` directory to create schemas in BigQuery that are prefixed with `mart_`

### 4.3. Confirm DBT project tree

Your DBT project structure should now look like this (`target` may or may not have sub directories, depending on whether you've already run some models - don't worry too much about that directory)
```
.
├── README.md
├── analyses
├── data
├── dbt_project.yml
├── macros
│   ├── meta
│   └── models
├── models
│   ├── example
│   │   ├── my_first_dbt_model.sql
│   │   ├── my_second_dbt_model.sql
│   │   └── schema.yml
│   ├── mart
│   ├── source
│   └── staging
├── snapshots
└── tests
```

<br>

# 5️⃣ Run your first models and tests 🧪

Your setup is now ready to run your first models!
- Execute the following command to generate your models:
  - `dbt run -m my_first_dbt_model`
    If you've understood well the instructions: do you know where this model will be created in BigQuery?
  - `dbt run -m my_second_dbt_model`
  - `my_second_dbt_model` is dependent on `my_first_dbt_model`. If you want to refresh `my_second_dbt_model` having `my_first_dbt_model` being refreshed first, run the following command:
     `dbt run -m +my_second_dbt_model`
- As seen in `dbt_lewagon/models/example/schema.yml`:
  - `id` in `my_first_dbt_model` should be `unique` and `not_null`
  - `id` in `my_second_dbt_model` should be `unique` and `not_null`
- Let's verify that by running those tests:
  - `dbt test -m my_first_dbt_model`
  - `dbt test -m my_second_dbt_model`
- In the BigQuery interface, in your personal dataset, go check that
  - `my_first_dbt_model` is a table
  - `my_second_dbt_model` is a view - this matches what you've written in the config of each of your models

<br>

# 🏁 Finishing up

Congratulations on setting up your first DBT project and running some models! The setup was lengthy, but this is a great foundation for any future DBT project you may have!

🧪 Test your setup with:

```
make test
```

And make sure to add, commit, and push your code up to github so your progress is tracked on Kitt!

## Some DBT Tips 💡

If you want to refresh all your models, or run all your tests, no need to specify the model with the `-m xxxx` parameter:
- `dbt run` refreshes all your DBT models
- `dbt test` runs all the tests configured in the project

Remember the tests you implemented in SQL in `0203-SQL-Advanced`? The concept of a SQL test was "it fails if the SQL query returns at least 1 record". Go and check the actual "compiled" tests that DBT has interpreted by going to `target/run/dbt_lewagon/models/example/schema.yml/`. This is where you'll find the tests that come directly from the setup done in the `schema.yml` file. If you open one of the unicity tests, like `unique_my_first_dbt_model_id.sql`, you'll see it has the classic structure:

```sql
select
    unique_field,
    count(*) as n_records
from dbt_test__target
group by unique_field
having count(*) > 1
```
