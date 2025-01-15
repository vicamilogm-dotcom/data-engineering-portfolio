# 🎯 Goal

We need to explore the dataset available. This should be done in 3 steps
  - Understand the structure of the tables and the data types of the fields in those tables.
  - Understand the concept of the primary key, foreign key, and field constraints.
  - Explore the data contained in the tables, make sure it's coherent and respects the constraints associated to their definitions (introducing the concept of SQL tests implemented on a data pipeline).

Concepts:
- DB Schema.
- Single table operations - SELECT, FROM, WHERE, GROUP BY, HAVING, ORDER BY
- JOINs.

# Tasks

First, copy you `.env` file from the previous challenge inside this challenge's folder. We'll need it to run the tests, which will connect to your database.

## DB schema analysis

**❓ Write a query that provides the list of tables in the "movies" database**.
- Notice that 2 tables are "public" (the one you created), while many other are internal to postgres!
- Try to filter them to only get 2 rows.
- Store your code in `exercice-1.sql`.

**❓ Write a query that returns the list of columns and their data types in the `movies_metadata` table.**
- You should have a (24,2) table as a result.
- Store your code in `exercice-2.sql`.

## SQL tests

💡 The way to write a test in SQL is to write a query that returns rows if the test fails, and no row if the test succeeds. You will see later in the bootcamp how DBT uses this type of tests in your ETL pipeline.

The `adult` column is a boolean column. Meaning its values should only be TRUE, or FALSE. **❓ Write a query that makes sure that this column is never equal to any other value**. Store your code in `exercice-3.sql`.


**❓ Write a test that checks the unicity of the `id` column in the `movies_metadata` table.**
- It fails if 2 records in this table share the same `id` (if it's indeed unique, then ID can be called a primary key).
- The output of your query should be a table with 2 columns : `id`, `num_records`
- 🧪 Store your code in `exercice-4-1.sql` and run `pytest tests/exercice-4_1.py` in your terminal to check your results.

❓ Can you give more context when it fails, by adding movies metadata to the previous query? It will help you visually compare pairs of rows that have the same ids, and help explain what caused some records to be duplicated!
<details>
  <summary markdown='span'>💡 Hints</summary>

💡 Re-use your previously computed table, and join it with the `movies_metadata`!
You'll see that one column duplication of the ID seems to regularly be coming from a difference in "popularity"
</details>

- Store your code in `exercice-4-2.sql`

**❓ Write a test that checks for referential integrity between the two tables**

- The `movie_id` column in the `ratings` table should refer to the `id` column in the `movies` table.

<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/movie_db_schema.png" width=250>

- One movie can have many ratings (1 -> N relationship). 🤔 There would be a problem if a `movie_id` in the `ratings` table did not exist in the `movies` table

👉 Check whether this happens or not:
- The output of the query should be 1 column, called `movie_id_ratings_table`, which lists all the *distinct* `movie_id` that exist in the `ratings` table *but don't exist* in the `movies_metadata` table.
- This query should take ~ 10 seconds to execute - and it will also increase the duration of your tests execution, so make sure you do this exercise at the end.
- Store your code in `exercice-5.sql`


🏁 🧪 `make test` to check all your results. Commit and push your code so your progress is updated on Kitt!
