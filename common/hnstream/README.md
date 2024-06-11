# Hacker News streamer

## Dataset

BigQuery `bigquery-public-data.hacker_news`.

Schema, coming from

```[sql]
SELECT * EXCEPT(is_generated, generation_expression, is_stored, is_updatable)
FROM `bigquery-public-data.hacker_news`.INFORMATION_SCHEMA.COLUMNS
WHERE table_name="<insert table name here>"
```

**Table `stories`**

```
    column_name  data_type
0            id      INT64
1            by     STRING
2         score      INT64
3          time      INT64
4       time_ts  TIMESTAMP
5         title     STRING
6           url     STRING
7          text     STRING
8       deleted       BOOL
9          dead       BOOL
10  descendants      INT64
11       author     STRING
```

**Table `comments`**

```
  column_name  data_type
0          id      INT64
1          by     STRING
2      author     STRING
3        time      INT64
4     time_ts  TIMESTAMP
5        text     STRING
6      parent      INT64
7     deleted       BOOL
8        dead       BOOL
9     ranking      INT64
```

## How to use

Encode your GCP JSON credentials with BigQuery access to base64  and store this value to the environment variable `GCP_CREDS_JSON_BASE64`. Here's a one-liner to do it `export GCP_CREDS_JSON_BASE64=$(eval base64 -i /path/to/gcp-creds.json)`.

- Build the container with `make build`
- Run it with `docker run --rm -e GCP_CREDS_JSON_BASE64=<base 64 encoded GCP credentials JSON file> -p 50051:50051 lewagon/hnstream:0.1.0`
- The server is now accessible on your server/machine's port 50051
- You can access it with a generated client. Test it with `poetry run python client.py` on your machine.

**Create a client, run a query and return a Pandas DataFrame**
```
from hnstream import bq

client = bq.get_client()

query = """
SELECT title, time_ts
FROM `bigquery-public-data.hacker_news.stories`
WHERE REGEXP_CONTAINS(title, r"(k|K)aggle")
ORDER BY time
LIMIT 30
"""

bq.query_as_df(client, query)
```

or using the `queries` module

```
from hnstream import bq, queries

client = bq.get_client()
query, params = queries.table_metadata("stories")

bq.query_as_df(client, query, query_parameters=params)
```
