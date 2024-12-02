# ❗ Legacy Challenge ❗

This is a legacy challenge and has been archived as is.

It has been left available if you want to practice, but will not contribute towards your mandatory challenge completion percentage as part of the Le Wagon Data Engineering Bootcamp.

If you want to do these challenges, here are a few notes:
- The `pyproject.toml` has been renamed to `pyproject.toml.bak`.
    - This was done so that a virtual environment for this challenge was not installed when your ran `make install` on Setup Day, reducing disk usage.
    - If you want to install the poetry virtual environment, rename the `pyproject.toml.bak` to `pyproject.toml` and run: `poetry install`
    - You may need change the path of the package: `lewagonde` in the `pyproject.toml`. `lewagonde` contains helper functions for testing.
- Consider creating a new dbt profile for these challenges. Such as: `dbt_hackernews`

# 🎯 Goals

This unit's challenges follow on from each other. Piece by piece, you will build a robust DBT project. As an overview, here is what we'll be doing in each challenge:
- In `01-Setup-DBT` - you've built the initial structure, added files to it
- In `02-DBT-Basics` - you'll create your first staging models, refined versions of the `source` data that comes from the public BigQuery dataset
- In `02-DBT-Advanced` - create models on top of the `staging` models, implement tests, and document our models to make it more understandable for stakeholders.

You'll create your first models in staging, which are refined versions of the `source` data inherited from the BigQuery dataset.

Let's get to configuring your sources and creating your first staging models! 🚀

## 🧪 A note on tests

The tests for this unit are testing against real BigQuery tables and views that your DBT models create in each challenge, or by checking the file structure of `0x-xxx/dbt_lewagon` folder. Make sure that your solutions are always in the `dbt_lewagon` project of the current challenge.

As always, feel free to have a look in the `tests/` directory and see how the tests are working!

<br>

# 0️⃣ Setup

We'll be using the same DBT project for each challenge, so lets start by copying the `dbt_lewagon` from the previous challenge, `01-Setup-DBT`, to the current challenge root.

<br>

# 1️⃣ Configuring your sources

We'll start with configuring the data sources, where DBT is retrieving our data, and what our models will work with.

- Under the `models/source` folder, create a file named `src_hackernews.yml`. This is where you'll configure the reference to the BigQuery public dataset: HackerNews.
- Populate this file so that it understands:
  - in which BQ project it's located
  - in which BQ dataset it's located
  - what are the tables from this data we should be pulling
  - You should follow this documentation to understand how to configure a source in DBT:
    - [Source properties](https://docs.getdbt.com/reference/source-properties)
    - [Source Configuration - database](https://docs.getdbt.com/reference/resource-properties/database)
- You should configure 3 sources:
  - the `full` table
  - the `comments` table
  - the `stories` table

<br>

# 2️⃣ Configuring your first staging model

Let's start with configuring your first staging model that reads from the `full` source.

- Under the `models/staging/` folder, create a file called `stg_hackernews_full.sql`.
- Configure this model this way:
  - It should be a `table` materialization
  - It should simply be reading from the `bigquery-public-data.hacker_news.full` table.
  - Keep all the columns but rename some of them:
    - `url` to `original_url`
    - `dead` to `is_dead`
    - `by` to `author`
    - `parent` to `parent_id`
    - `deleted` to `is_deleted`
  - Convert the `timestamp` field into a `DATETIME`, in the `America/Los_Angeles` timezone, and call the field `created_at_local`
  - Add a column called `row_created_at_local` which logs the `CURRENT_DATETIME` at which the row is created in the table, in the `America/Los_Angeles` timezone
  - Filter the records
    - Remove records that are "dead"
    - only keep the data that was `created_at_local` in the last 1000 days of data

  <details>
    <summary markdown='span'>💡 Hint</summary>
    You can you can use the `DATE_SUB` SQL function
  </details>

- Run this model by executing the following command in your terminal: `dbt run -m stg_hackernews_full` and check that it's been created in BigQuery: `dbt run -m stg_hackernews_full`
- 🧪 Run `make test_hackernews_full` - 2 tests should have passed:
  - `test_hackernews_full_structure`
  - `test_hackernews_full_content`

<br>

# 3️⃣ Configure `stg_hackernews_comment.sql`

The second staging model will source data from the `comments` source.

- Under the `models/staging/` folder, create a file called `stg_hackernews_comment.sql`.
- Make this model
  - a `table`
  - which reads from `stg_hackernews_full`
  - filters only news that are a `comment`
- Column renaming - rename the following columns:
  - `id` becomes `comment_id`
  - `parent_id` becomes `comment_parent_id`
  - and keep only a subset of columns so that your final list of fields is:
  ```sql
    comment_id
  , comment_parent_id
  , author
  , created_at_local
  , text
  , original_url
  , is_deleted
  , is_dead
  , ranking
  , row_created_at_local
  ```
- Run this model: `dbt run -m stg_hackernews_comment`

<br>

# 4️⃣ Configure `stg_hackernews_story.sql`

Finally, let's create our last staging model that retrieves data from the `story` source.

- Under the `models/staging/` folder, create a file called `stg_hackernews_story.sql`.
- Make this model
  - a `table`
  - which reads from `stg_hackernews_full`
  - filters only news that are a `story`
- Column renaming: you can rename the columns
  - `id` becomes `story_id`
  - and keep only a subset of columns so that your final list of fields is:

- Your final list of columns should be:
  ```sql
    story_id
  , title
  , author
  , created_at_local
  , text
  , original_url
  , is_deleted
  , is_dead
  , ranking
  , row_created_at_local
  ```
- Run this model: `dbt run -m stg_hackernews_story`
- 🧪 Run `make test_hackernews_story_comment`: two tests should have passed:
  - `test_hackernews_story_structure`
  - `test_hackernews_comment_structure`
- You can now run all tests: run `make test`

<br>

# 🏁 Finishing up

Congratulations! You've now configured your sources and created staging models for those sources!

A recap of what you've done in this challenge.

- DBT is now able to identify the source data (the Hackernews public dataset), and pull from it
- You've created 3 models
  - `stg_hackernews_full`: which is a clean version of all the stories, comments etc that have been written on Hackernews
  -  `stg_hackernews_comment`: a subset of the full model. Only displaying the comments.
  -  `stg_hackernews_story`: a subset of the full model. Only displaying the stories.
  - Why split the `full` model? Because for some use cases, we will run some analysis specifically on the stories or on the comments, and we don't want to ping a massive table everytime. But rather separate the information.

🧪 If you haven't, run `make test`, git add, commit, and push your code to github so our can track your progress on Kitt!

<br>
