# 🏁 Accelerating a postgres database with indexing

Database access patterns determine what to optimize for. A database gives us many tools to make queries more efficient. Assuming the data schema is sensible, adding indexes to the database is the next best thing to work on, that's what will keep us busy in this exercise.

We will use our beloved Postgres database, and load the [Ikea dataset](https://www.kaggle.com/datasets/crawlfeeds/ikea-us-products-dataset).

<br>

# 0️⃣ Setup

In this exercise, we'll build the functions one by one in `lwdb/db.py` and open them in an IPython notebook `challenge.ipynb`

❓ First, download the data under `./data/ikea-raw.json`.

<details>
<summary markdown='span'>💡 Hint</summary>

Use `wget` or `scp` from the CHEATSHEET.md
</details>

<br>

# 1️⃣ Data Loading

## 1.1. Investigate data

❓ Do you know a way to inspect your JSON in the CLI?

<details>
<summary markdown='span'>💡 Hint</summary>

Look at a first few lines of the JSON, in the command line do:
```bash
cat ./data/ikea-raw.json | python -m json.tool | head -n20
# or
cat ./data/ikea-raw.json | jq '.' | head -n20
```
</details>

❓ Let's investigate it with Pandas first by loading the JSON to Pandas in the  `challenge.ipynb` notebook. Look at the columns, do they look like they all have the right type? Cast the 3 numerical columns (`product_price`, `average_rating`, `reviews_count`) with string type to `float` or `"Int64"` using `pandas.to_numeric` and `df[column].astype("Int64")`.

❓ Save this DataFrame in two following formats, then compare disk space with `du` linux tool and conclude!
- "data/ikea-cols.parquet" (column major format)
- "data/ikea-rows.csv" (row major format)

## 1.2. Create a database

❓ **create a new database** named `ikea` using `psql` in your terminal!

❓ **Create the schema** by mapping the CSV schema using `./sql/prep_schema.sql` that is already provided.

You can execute the sql commands from DBeaver, or from your terminal with:

```bash
psql -d ikea
```

❓ **Load the CSV data** into the Postgres table!

🧪 `Make test` should pass few more tests

<br>

# 2️⃣ Querying

## 2.1. Without indexing
Let's write a few queries to this medium-sized database to test their speed.
- Test the query speed by calling `query_perf(file_path="xxx.sql")` from your notebook.

**❓ Select product with SKU "693.885.84"**

**❓ Count the number of products** mentioning the words `chair` and `armrest` in the `raw_product_details` column.
- Write the query to `sql/search-chair.sql`

How long did it take the query to execute? Do you think we can do better? Let's try!

## 2.2. With indexing

❓Add a BTree index on SKU named `index_sku` to the file `index_btree.sql` and run it.

Nothing better than the official [Postgres documentation](https://www.postgresql.org/docs/current/sql-createindex.html) to figure out how to create the index 🙌.

<details>
<summary markdown='span'>💡 Hint</summary>

Indexes are BTrees by default.
</details>

Now run the first query again, is it faster?

## 2.3. Full-text search engine

❓ First of all, the `raw_product_details` column is HTML, not super friendly to search into. Let's create a new column `raw_product_details_text` and extract only the text from this HTML. You can use the SQL transformation below for the new column:

```sql
regexp_replace(raw_product_details, E'<[^>]+>', ' ', 'gi')
```

<details>
<summary markdown='span'>💡 Hint</summary>

- First create the column `raw_product_details_text`.
- Then update its values using the transformation above.
</details>

❓ Add the SQL code in `sql/add_text_col.sql`.

Now that we have a suitable text column, we'd like to add a **search engine** to our database! It would be nice to search for keywords in the product details.

Postgres can index keywords efficiently in text columns using the `GIN` index on a `tsvector`. Essentially, text is parsed into a [tsvector](https://www.postgresql.org/docs/current/datatype-textsearch.html) (check out the examples to understand how Postgres reads text vectors). Then, a GIN index is used to speed up lookups by keywords.

Read the [official documentation, section 12.2.2](https://www.postgresql.org/docs/current/textsearch-tables.html#TEXTSEARCH-TABLES-INDEX).

Note that there are two ways to index a text column. Either index it directly by having an on-the-fly transform to `tsvector`, OR (recommended) create a `tsvector` column, then index that column with the GIN index.

We'll follow the second method. Add the new `tsvector` column, name it `textsearchable_raw_product_details_text`, and then index it with the GIN index. Call the index `index_raw_product_details_text`. It's a bit hard, so after giving it a shot first, please feel free to check out the walk through hint below 👇.

<details>
<summary markdown='span'>💡 Hint</summary>

First create the column

```sql
ALTER TABLE <table name>
ADD COLUMN <new tsvector column name> tsvector
GENERATED ALWAYS AS (to_tsvector('english', <text column name>)) STORED;
```

then add the index

```sql
CREATE INDEX <index name>
ON <table name>
USING GIN (<new tsvector column name>);
```
</details>

Now rewrite the second query as as `sql/search-chair-indexed.sql`. The [bottom of the official documentation, section 12.2.2](https://www.postgresql.org/docs/current/textsearch-tables.html#TEXTSEARCH-TABLES-INDEX) tells you all about running fast text queries against the `tsvector`, indexed column.

<details>
<summary markdown='span'>💡 Hint</summary>

Break down the query as:

```sql
SELECT count(*)
FROM ikea_products
WHERE textsearchable_raw_product_details_text @@ to_tsquery('chair & armrest');
```
</details>

Re-run it, is it faster?

<br>

# 3️⃣ (Optional) Bonus questions

- Time the CSV load with and without the SKU index. Notice any difference?

<details>
<summary markdown='span'>💡 Hint</summary>

It's good practice to first drop the index, load a large dataset, then re-apply the index if load performance is key.
</details>

<br>
