## High level goal

You'll create your first models in staging, which are refined versions of the `source` data inherited from the BigQuery dataset

## 1️⃣ Instructions

:rotating_light: _Please read this carefully : it gives you information about how you'll do your challenges today_ :rotating_light:

- There's a continuity in today's challenges, where little by little, you're building a robust DBT project:
  - In `01-Setup-DBT`: you've built the initial structure, added files to it
  - In `02-DBT-Basics`, you'll do copy the whole `dbt_lewagon` directory from `01-Setup-DBT` into `02-DBT-Basics`
  - In `03-DBT-Advanced`, copy  `02-DBT-Basics` into `03-DBT-Advanced`
  - etc...

- Our tests are testing against the real BigQuery models you're supposed to create in each challenge, or checking the file structure of `0x-xxx/dbt_lewagon` folder

- Store your answers always in the `dbt_lewagon` project of your current challenge.

❓ So, **first copy `dbt_lewagon` from the previous challenge section into this one_**

## 2️⃣ Configuring your sources

- Under the `models/source` folder, create a file named `src_hackernews.yml`. This is where you'll configure the reference to the BigQuery public dataset : HackerNews.
- Populate this file so that it understands :
  - in which BQ project it's located
  - in which BQ dataset it's located
  - what are the tables from this data we should be pulling
  - You should follow this documentation to understand how to configure a source in DBT :
    - [Source properties](https://docs.getdbt.com/reference/source-properties)
    - [Source Configuration - database](https://docs.getdbt.com/reference/resource-properties/database)
- You should configure 3 sources :
  - the `full` table
  - the `comments` table
  - the `stories` table

## 3️⃣ Configuring your first staging model

- Under the `models/staging/` folder, create a file called `stg_hackernews_full.sql`.
- Configure this model this way :
  - It should be a `table` materialization
  - It should simply be reading from the `bigquery-public-data.hacker_news.full` table.
  - Keep all the columns but rename some of them :
    - `url` to `original_url`
    - `dead` to `is_dead`
    - `by` to `author`
    - `parent` to `parent_id`
    - `deleted` to `is_deleted`
  - Convert the `timestamp` field into a `DATETIME`, in the `America/Los_Angeles` timezone, and call the field `created_at_local`
  - Add a column called `row_created_at_local` which logs the `CURRENT_DATETIME` at which the row is created in the table, in the `America/Los_Angeles` timezone
  - Filter the records
    - get rid of the records that are "dead"
    - only keep the data that was `created_at_local` in the last 1000 days of data

  <details>
    <summary markdown='span'>💡 Hint</summary>
    You can you can use the `DATE_SUB` SQL function
  </details>

- Run this model by executing the following command in your terminal : `dbt run -m stg_hackernews_full` and check that it's been created in BigQuery : `dbt run -m stg_hackernews_full`
- 🧪 Run `make test_hackernews_full` : 2 tests should have passed :
  - `test_hackernews_full_structure`, and
  - `test_hackernews_full_content`

## 4️⃣ Configure `stg_hackernews_comment.sql`

- Under the `models/staging/` folder, create a file called `stg_hackernews_comment.sql`.
- Make this model
  - a `table`
  - which reads from `stg_hackernews_full`
  - filters only news that are a `comment`
- Column renaming : you can rename the columns
  - `id` becomes `comment_id`
  - `parent_id` becomes `comment_parent_id`
  - and keep only a subset of columns so that your final list of fields is :
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
- Run this model : `dbt run -m stg_hackernews_comment`

## 5️⃣ Configure `stg_hackernews_story.sql`
- Under the `models/staging/` folder, create a file called `stg_hackernews_story.sql`.
- Make this model
  - a `table`
  - which reads from `stg_hackernews_full`
  - filters only news that are a `story`
- Column renaming : you can rename the columns
  - `id` becomes `story_id`
  - and keep only a subset of columns so that your final list of fields is :

- Hence your final list of columns should be :
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
- Run this model : `dbt run -m stg_hackernews_story`
- 🧪 Run `make test_hackernews_story_comment` : 2 tests should have passed :
  - `test_hackernews_story_structure`, and
  - `test_hackernews_comment_structure`
- You can now run all tests and generate the test outputs : run `make test`
- Push to git

## Summary

- DBT is now able to identify the source data (the Hackernews public dataset), and pull from it
- You've created 3 models
  - `stg_hackernews_full` : which is a clean version of all the stories, comments etc that have been written on Hackernews
  -  `stg_hackernews_comment` : a subset of the full model. Only displaying the comments.
  -  `stg_hackernews_story` : a subset of the full model. Only displaying the stories.
  - Why split the `full` model ? Because for some use cases, we will run some analysis specifically on the stories or on the comments, and we don't want to ping a massive table everytime. But rather separate the information.
