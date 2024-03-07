# Chatroom analytics

🎯 We have our chatroom but now we need to add a database to collect the messages in realtime, we will do this using clickhouse!

## Setup clickhouse

First you need to setup clickhouse with the following requirements:

1. User named `rmq`
2. Password from an enviroment variable `CLICKHOUSE_PASSWORD`
3. Uses the image `clickhouse/clickhouse-server:23.7.4.5-alpine`

❓ Update the docker compose to achieve this

Once you are done check your progress with:

```bash
make test
```

## Setup the table

Now we need to setup a table named `user_messages` to store our messages which will store
the `username`, `message`, and `received_at`!

❓ Workout how to connect to the db and create the table

A good starting point are the docs https://clickhouse.com/docs/en/sql-reference/statements/create/table


<details>
<summary markdown='span'>💡 Solution </summary>

```sql
CREATE TABLE IF NOT EXISTS chat.user_messages (
    username String,
    message String,
    received_at DateTime
) ENGINE = MergeTree() ORDER BY received_at
```

If you can't workout where to run this think of how we did it with postgres and the `psql` command!

</details>

Now we are ready to begin using rabbitmq to automate the insertions!

## Create the callback

Now we have a table we want to write each message received into our clickhouse table. The initial approach would be to rewrite our callback to index at the same time. At smaller scales this would work fine but would defeat the benefits gained by using a messaging queue.

- Putting it into the message displays may at some point slow our app.
- Decoupling the messaging and indexing allows us to scale each part separately for example if we wanted to do some complex transformations at scale.
- Our database crashing will not stop our app with this approach!

Instead what we will do is called a fanout exchange

<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W3D4/exchange-fanout.png" width=700>

The idea here is that messages are sent to the central exchange and then sent to all of the queues. This allows each queue to deal with the message at its own pace. For example if the database crashes its queue would keep all of the messages but they could be consumed by the messaging display queue so the app continues to work and when the database is recovered they can still be indexed!

Here the exchange has already been setup for you:

❓ Code `clickhouse_callback` following the doc string inside `rabbitmq_clickhouse.py`

Once this is done run both the original subscriber and the new clickhouse subscriber

```bash
python lwqueue/rabbitmq_subscriber.py --host localhost --port 5672 --mode rich --rmq-username rmq --rmq-password $RABBITMQ_DEFAULT_PASS
python lwqueue/rabbitmq_clickhouse.py --host localhost --port 5672 --mode rich --rmq-username rmq --rmq-password $RABBITMQ_DEFAULT_PASS
```

Then send a message and check that it is displayed, you can check it is indexed by entering the db and doing a `SELECT *`!

Now lets populate the db with some quotes from the bot mode

```bash
python lwqueue/rabbitmq_send_message.py --host localhost --port 5672 --message "Hello world" --username $USER --rmq-username rmq --rmq-password $RABBITMQ_DEFAULT_PASS --bot
```

You should see the data being displayed and indexed!

## Query the data

One of the main reasons for using clickhouse is the ability to do fast real time analytics so lets create some queries to analyse our data!

Go to `clickhouse_queries.py` and we will fill out the functions:

### Query

❓ Code `query_clickhouse` to allow different queries to be passed as strings and run against your db!

### Messages

❓ Code `get_all_messages` in order to retrieve all of the messages

Once you are done run make sure to stop the bot to stop new data being added to the db and then:

```bash
make test
```

### Active users

❓ Code `get_top_active_users` following the docstring

Run:

```bash
make test
```

### Message gap

We want to check how active our chatroom is

❓ Code `get_average_message_gap` this will be quite a lot harder than in postgres (it is worth seeing limitations of clickhouse)

Once you are done 👇 and then push!

```bash
make test
```

## Finished 🏁

We now have a messaging app + analytics. This is a really powerful pattern and can be expanded to allow huge queues and large analytics at scale with ease!
