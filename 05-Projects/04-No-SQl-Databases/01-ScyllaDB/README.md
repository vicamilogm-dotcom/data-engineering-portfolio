# ScyllaDB

Scylla DB is one of the fastest growing databases. It is open source and builds on lots of the idea from cassandra We will quickly go through the basics in this readme

## Running one node

Lets start one node running **ScyllaDB**!

```bash
docker run --name node-a -d scylladb/scylla:4.5.0 --overprovisioned 1 --smp 1
```

Then we check that it is running

```bash
docker exec -it node-a nodetool status
```

It will take a little while when it is up the status should be **UN** which stands for Up/Normal which is the state a properly running node should be!

```bash
Datacenter: datacenter1
=======================
Status=Up/Down
|/ State=Normal/Leaving/Joining/Moving
--  Address     Load       Tokens       Owns    Host ID                               Rack
UN  172.17.0.3  160.1 KB   256          ?       0413d2ce-a5b8-458d-b960-86e25248b792  rack1
```
You can then enter the container in a shell similar to `psql`!

```bash
`docker exec -it node-a cqlsh`
```

There is not much purpose to **ScyllaDB** until we add a few more nodes!

## Adding more nodes

This command helpfully looks up the IPAddress of our first node so that the second and third we want to add know where to connect!

```bash
NODEA=$(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' node-a)
```

Now **add the nodes**!

```
docker run --name node-b -d scylladb/scylla:4.5.0 --seeds=$NODEA --overprovisioned 1 --smp 1
docker run --name node-c -d scylladb/scylla:4.5.0 --seeds=$NODEA --overprovisioned 1 --smp 1
```

Check until all the nodes are in a status `UN` using `docker exec -it node-a nodetool status` you will see they are `joining` for a little while before they enter the correct status!

## Adding some information

We have a small cluster now lets actually add some data!

```bash
docker exec -it node-c cqlsh
```

First we create a `keyspace` which is equivalent to a `database` in SQL!

```bash
CREATE KEYSPACE mykeyspace WITH REPLICATION = { 'class' : 'NetworkTopologyStrategy', 'replication_factor' : 3};
```

We define the `replication_factor` as three so that the data is put into all three of our nodes! We then select the namespace.

```bash
USE mykeyspace
```

Lets create a small users table everything here is similar to SQL but it is [CQL](https://www.scylladb.com/glossary/cassandra-query-language-cql/)!

```sql
CREATE TABLE users (
    user_id int,
    name text,
    age int,
    PRIMARY KEY (user_id)
);
```

With ScyllaDB **the PRIMARY KEY is very important** we will see why later! Lets add some data:

```sql
INSERT INTO users(user_id, name, age) values (1, 'Jeff', 35);
INSERT INTO users(user_id, name, age) values (2, 'Tim', 50);
```

Lets fetch our `users`

```sql
SELECT * FROM users;
```

Now lets try to filter by age 👇

```bash
cqlsh:mykeyspace> SELECT * FROM users WHERE age < 40
              ... ;
InvalidRequest: Error from server: code=2200 [Invalid query] message="Cannot execute this query as it might involve data filtering and thus may have unpredictable performance. If you want to execute this query despite the performance unpredictability, use ALLOW FILTERING"
```

ScyllaDB does not allow this by default because it does not know where the data is stored and so will have to do a linear scan of all of the nodes to check which takes forever! When you design a wide column db it is very important that you decide what you will query in advance. They are optimised for writes but not for analytical queries!

<br>

# 🏁 Finishing Up

If you want to dig deeper into wide column dbs ScyllaDB provides extensive learning resources on their website: https://university.scylladb.com/

<br>
