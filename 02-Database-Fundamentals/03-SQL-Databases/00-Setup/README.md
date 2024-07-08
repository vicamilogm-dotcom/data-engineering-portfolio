# 🎯 Goal

Lets start today by setting up our own postgres database on our Virtual Machine and connecting to it via DBeaver on our local machine!

Compared to previous units, there are a few key differences in *where* we'll be running postgres in challenges for this unit. In previous units, we ran postgres in a docker container. In this unit we will be running postgres directly on our virtual machine! It's a small but important difference, but it means there are some additional steps because the base postgres docker image has an initialisation script that does some set up for us. When running postgres directly on our VM, we'll have some additional configuration to do!

In production environments, it's not uncommon to have self managed databases running on a dedicated server (or VM) without docker, so it's important to understand how they are set up!

In this challenge we will:
- Craete a new user in postgres
- Create a new database in postgres
- Create tables in a postgres database
- Load data into those tables from CSV's
- Connect postgres running on our Virtual Machine to DBeaver on our local computer

💡 This challenge was designed as a postgres reference, and still applies if you are running postgres in container. Think about bookmarking this challenge for future reference!

Let's get to creating our database! 🐘🚀

<br>

# 0️⃣ Getting started

We installed postgres and saw that it was running as a service on setup day, but lets check that it is still running and active!

```bash
service postgresql status
```

If it is not running:

<details>
<summary markdown='span'>💡 Restart!</summary>

```bash
sudo service postgresql restart
```

</details>

<br>

# 1️⃣ Creating a new user

## 1.1. Connecting

The simplest way to interact with postgres is with its terminal based front-end: [psql](https://www.postgresql.org/docs/current/app-psql.html)

Try connect with:

```bash
psql postgres
# try to connect to the default postgres database inside your postgres instance
```

You should see an error similar to the below:

![user_does_not_exist](https://wagon-public-assets.s3.eu-west-3.amazonaws.com/239cegfj36yjvmtlm8vap98iwsq1)

❓ Why? There is a few things that are worth noting:
- On a clean install of postgres, by default it only one user and one database - both are named **postgres**.
- `psql` will try to connect to the database as a **postgres user** with the same name as your current *linux username* - but it doesn't exist as a user inside our postgres instance!

To make our workflow as easy as possible, we need to create a **postgres user** that matches our *linux username*. But how do we get access to postgres?

Luckily, there is a *linux user* on our virtual machine called "postgres". Let's login as the "postgres" *linux user* to create our new **postgres user**.

```bash
sudo --login --user=postgres psql
# for more info on this command, run: tldr sudo
```

☝️ we are logging in as the "postgres" *linux user*, allowing us to log directly in as the "postgres" user on the database. You should have entered the `psql` shell and be able to interact with postgres.

## 1.2. Create a new user and password

For ease, we can create a postgres user with the same username as our linux system username (type `whoami` or `echo $USER` in a regular terminal to get your linux username).

```bash
CREATE USER <username> WITH SUPERUSER PASSWORD 'choose a password here';
# 🚨 Don't forget the ; (semi-column) at the end
# it's mandatory when executing statements in psql
```

☝️ We have created this **postgres user** as a _superuser_, but in general you should try to only assign the appropriate [role attributes](https://www.postgresql.org/docs/current/role-attributes.html). For example, creating a user with the appropriate connection limit to prevent your database being overwhelmed.

To check you've created the user, run the following in a `psql` shell:

```bash
\du
```

💡 This `\du` is a special `psql` command to shortcut important actions known as [meta commands](https://www.postgresql.org/docs/current/app-psql.html)!

👉 Write down your postgres user password in a `.env` file in this challenge folder. We'll need it later on.

```bash
#.env
POSTGRES_PASSWORD='the password you just chose'
```

We now have our **postgres user**! 🎉

Now let's log out of postgres (as the _linux_ "postgres" user and "postgres" **postgres user**) and log back in to postgres as the new user we just created. First we need to exit the current `psql` session, use the following meta command:

```bash
\q
```

Now we can log back in with our newly created user. Since we created with the same name as our *linux* username, we can run:

```bash
psql postgres
# equivalent to `psql --username=$USER postgres`
```

Let's check our current user with an SQL query:

```sql
SELECT current_user;
```

If the above query returns your *linux username* then you are good to go!

That can be a bit of a tricky process and it is hard to articulate in words. Here is an image that illustrates what we just did that might help!

![create new user](https://wagon-public-assets.s3.eu-west-3.amazonaws.com/wt5h5n2r8y08f9brdywc3ht74ohj)

<br>

# 2️⃣ Creating a Database and Tables

## 2.1. Creating a Database

Logged in as our new user, our next step is to create a new database! In a `psql` shell:

```sql
CREATE DATABASE school;
```

If we list the databases, you should see your newly created `school` database. Use the following meta command to list all databases:

```bash
\l
```

Let's connect to the `school` database instead of the default postgres database:

```bash
\c school
```

We can see what tables exist in the `school` database with the following meta command:

```bash
\d
```

None should be returned. Let's create some tables and insert some records in postgres next.

## 2.2. Creating tables

One way would be with a sql script:

```sql
CREATE TABLE students (
    id          INTEGER PRIMARY KEY,
    first_name  VARCHAR(40) NOT NULL,
    last_name   VARCHAR(40) NOT NULL,
    batch_num   INTEGER
);

INSERT INTO students (
    id
    , first_name
    , last_name
    , batch_num
)
VALUES
      (1, 'Zinedine', 'Zidane', 101)
    , (2, 'Kelly', 'Slater', 101);
```

If you run this query and then run `\d`, you should now see a `students` table, which you can now query:

```sql
SELECT * FROM students;
```

<br>

# 3️⃣ Connecting to DBeaver

While `psql` is very powerful, it would be easier for us to work in a more user focused tool, especially as our queries get more complicated. We'll use [DBeaver](https://dbeaver.io/) as our SQL client - but to get the data from our `postgres` server hosted on our Virtual Machine to DBeaver on our local computer, we need to forward some ports!

First, let's check which port our postgres server is running on (default is 5432) with the following meta command in `psql`:

```bash
\conninfo
```

We need to make that port available on our local machine so DBeaver can access the data in the database. A bit like the image below!

![postgres_vm_local_dbeaver](https://wagon-public-assets.s3.eu-west-3.amazonaws.com/r5i5yy7of1e3x95yc16eza1ljbfn)

#### Step 1:

In VSCode, click on `PORTS` next to your `TERMINAL` section.

![ports tab](https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W0D3/ports-tab.png)

<br>

#### Step 2:

Enter 5432, and press Enter. By default, VSCode auto populates the Local Address section with the value `localhost:5432` - the corresponding port on your local computer.
If you see a different value then 5432, port 5432 on your local machine is probably occupied by another service, that is totally fine. You can use any local port number.

At this point, port 5432 on your virtual machine is being forwarded to port 5432 on your local machine.

![forwarded port](https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W0D3/forwarded-port.png)

<br>

#### Step 3:

Open DBeaver and click the new connection button in the top left, then select postgres.

![new conn](https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W0D3/dbeaver-new-conn.png)

<br>

#### Step 4:

Fill out the postgres connection page. Key inputs are in the red boxes:

- Database: school
- Port: the port you forwarded to
- Username: your created user
- Password: your created password (check your `.env`!)

<br>

![postgres connection](https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W0D3/postgres-connection.png)

#### Step 5:

You should now see the database on the navigator at the side. Create a script and rerun our original query. You should see the same output as when you ran it in `psql`.

![connected](https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W0D3/connected-dbeaver.png)

<br>

# 4️⃣ Bringing in data

We are up and running in DBeaver! Time to bring in data from external source. Let's load `teacher.csv` into a new table in our db!

We need to create a table that the teacher data will be inserted into. This table will have 2 columns: `id` - which will be an integer, and `name` - a variable length character type, that we will limit to 50 characters.

The list of all possible Postgres data types is [here](https://www.postgresql.org/docs/current/datatype.html).

Run the following script to create this table:

```sql
CREATE TABLE teachers (
      id      INTEGER
    , name    VARCHAR(50)
);
```

If you run this script again, it should fail with the error: `relation "teachers" already exists`. That is why we generally don’t use the `CREATE TABLE` statement by itself. It is more common to use it with another command depending on the use case.

If we didn't want to overwrite an existing table, we could check to see if the table already exists:
```sql
CREATE TABLE IF NOT EXISTS teachers (
      id      INTEGER
    , name    VARCHAR(50)
);
```

This will not do anything if the table has already been created.

Alternatively, we could fully delete the table and recreate it:
```sql
DROP TABLE IF EXISTS teachers;
CREATE TABLE teachers (
      id      INTEGER
    , name    VARCHAR(50)
);
```

Let's load the data from the CSV file into the table by running the follow command in `psql`:
```bash
# fist connect to psql
psql --user=your_db_superuser_name -d school
```
Then run:

<details>
<summary markdown='span'>💡 Quick way to get the absolute path for a file!</summary>

```bash
readlink -f
```
</details>

```sql
school=#
\copy teachers
FROM '/home/.../absolute/path/to/teacher.csv'
DELIMITER ','
CSV HEADER;
```

<br>

# 🏁 Checking your database structure

Now that our data has been copied into our tables, it is important to check the global structure of your database. Modern SQL clients enable a clean, high level view of the entirety of your database, with tree-like explorers and other features, but it can be good to confirm with a SQL query.

Execute the following in DBeaver to see a list of all columns in every table:

```sql
SELECT *
FROM INFORMATION_SCHEMA.COLUMNS
WHERE table_schema = 'public'
ORDER BY table_name, ordinal_position
```

We now have a fully functional postgres database and a workflow when we want to
create new databases and tables!

🧪 Run `make test` to create a `test_output.txt`, then git add, commit, and push so your progress is tracked on Kitt!

❓ How many times was the word "postgres" used in this challenge? 😛

<details>
<summary markdown='span'>🎁 Answer</summary>
56 🫠
</details>

<br>
