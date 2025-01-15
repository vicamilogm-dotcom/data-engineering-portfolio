# 🎯 Goal

We have our chatroom and users can send and receive messages, but now we want to add a database to collect the messages in realtime, we will do this using ClickHouse!

<br>

# 1️⃣ Setup ClickHouse

First you need to setup ClickHouse with the following requirements:

1. A ClickHouse user named `rmq`
2. The password for that user from an environment variable `CLICKHOUSE_PASSWORD`
3. Using the image `clickhouse/clickhouse-server:23.7.4.5-alpine`

❓ **Update your docker compose with a ClickHouse service**

Once you are done check your progress with:

```bash
make test
```

And spin up your docker compose stack!

<br>

# 2️⃣ Setup the table

Now we need to setup a table named `user_messages` to store our messages which will store
the `username`, `message`, and `received_at`!

❓ **Workout how to connect to the database and create the table**

<details>
<summary markdown='span'>💡 Docker exec reminder</summary>

To interactively connect to a container via docker:

```bash
docker exec -it <container_name> <some_command> <and_args>
```

ClickHouse has a utility very similar to `psql`. A good place to look would be the ClickHouse CLI docs at [this link](https://clickhouse.com/docs/en/interfaces/cli#interactive).
</details>

To create the table from **inside the ClickHouse instance**, a good starting point are the ClickHouse DDL docs at [this link](https://clickhouse.com/docs/en/sql-reference/statements/create/table).

<details>
<summary markdown='span'>🎁 Solution </summary>

```sql
CREATE TABLE IF NOT EXISTS chat.user_messages (
    username String,
    message String,
    received_at DateTime
) ENGINE = MergeTree() ORDER BY received_at
```
</details>

Confirm that the database and created using [ClickHouses SHOW statements](https://clickhouse.com/docs/en/sql-reference/statements/show).

Now we are ready to begin using rabbitmq to automate the insertions!

<br>

# 3️⃣ Create the callback

Now we have a table we want to write each message received into our ClickHouse table. The initial approach would be to rewrite our callback to index at the same time. At smaller scales this would work fine but would defeat the benefits gained by using a messaging queue.

- Putting it into the message displays may at some point slow our app.
- Decoupling the messaging and indexing allows us to scale each part separately for example if we wanted to do some complex transformations at scale.
- Our database crashing will not stop our app with this approach!

Instead what we will do is called a fanout exchange

<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W3D4/exchange-fanout.png" width=700>

The idea here is that messages are sent to the central exchange and then sent to all of the queues. This allows each queue to deal with the message at its own pace. For example if the database crashes its queue would keep all of the messages but they could be consumed by the messaging display queue so the app continues to work and when the database is recovered they can still be indexed!

Here the exchange has already been setup for you:

❓ **Complete** `clickhouse_callback` **following the doc string inside** `rabbitmq_clickhouse.py`

Once this is done run both the original subscriber and the new ClickHouse subscriber in separate terminals:

```bash
python lwqueue/rabbitmq_subscriber.py --host localhost --port 5672 --mode rich --rmq-username rmq --rmq-password $RABBITMQ_DEFAULT_PASS
```
```bash
python lwqueue/rabbitmq_clickhouse.py --host localhost --port 5672 --mode rich --rmq-username rmq --rmq-password $RABBITMQ_DEFAULT_PASS
```

Then send a message and check that it is displayed, you can check it is indexed by entering the database and doing a `SELECT *`!

Now lets populate the database with some quotes from the bot mode

```bash
python lwqueue/rabbitmq_send_message.py --host localhost --port 5672 --message "Hello world" --username $USER --rmq-username rmq --rmq-password $RABBITMQ_DEFAULT_PASS --bot
```

You should see the data being displayed and indexed!

<br>

# 4️⃣ Query the data

One of the main reasons for using ClickHouse is the ability to do fast real time analytics so lets create some queries to analyse our data!

Go to `clickhouse_queries.py` and we will fill out the functions. The tests will be running against your ClickHouse instance so make sure that it's still running!

### 4.1. Query

❓ **Code** `query_clickhouse` **to allow different queries to be passed as strings and run against your database!**

### 4.2. Messages

❓ **Code** `get_all_messages` **in order to retrieve all of the messages**

Once you are done run make sure to stop the bot to stop new data being added to the database and then run:

```bash
make test
```

### 4.3. Active users

❓ **Code** `get_top_active_users` **following the docstring**

Test with:

```bash
make test
```

### 4.4. Message gap

We want to check how active our chatroom is

❓ **Code** `get_average_message_gap`

👆 This will be quite a lot harder than in postgres. It is worth looking at the limitations of ClickHouse.

Once you are done, test it all with:

```bash
make test
```

<br>

# 🏁 Finishing up

We now have a messaging app and analytics! This is a really powerful pattern and can be expanded to allow huge queues and large analytics at scale with ease!

🧪 Test all your code with:

```bash
make test
```

And don't forget to git add, commit, and push to Github to track your progress on Kitt!

<br>
