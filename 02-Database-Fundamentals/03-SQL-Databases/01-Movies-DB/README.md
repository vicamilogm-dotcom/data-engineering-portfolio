# 🎯 Goal

You'll reproduce the steps done in `00-Setup` but with some more complex files. Make sure to reference the previous challenge if you get stuck. By the end of this challenge you'll be a pro at setting up postgres databases and tables! The goal is to have a database structure ready to execute SQL queries for the challenges `02-SQL-Basics` and `03-SQL-Advanced` in this unit.

We'll also look at some utilities for making the loading of data into databases a bit smoother!

<br>

# 0️⃣ Setup

## 0.1. Download

The [IMDB Movies dataset](https://wagon-public-datasets.s3.amazonaws.com/data-engineering/movies_dataset/archive.zip). The data that we'll be using for this, and the next few challenges.

Unzip and copy the two CSV's to your VM and into this challenge's subfolder: `./data/`

    - `movies_metadata.csv`
    - `ratings.csv`

You can copy them from you local computer to your VM with either `scp` (like a pro) or drag-and-drop (thanks to VSCode!)

Briefly explore the dataset on [Kaggle](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset?resource=download&select=ratings.csv) to get a feel for the tables and fields.

## 0.2. Create a database

Create a new postgres database called `movies`. We'll load the CSV's into individual tables a bit later.

A nice shortcut from the command line that does the job is:

```bash
createdb "movies"
```

Check that the `movies` table has been created with:
```bash
psql movies # then \l to list your databases and check you are the owner
```

## 0.3. Connect to DBeaver

Lastly, connect it to DBeaver exactly like we did in the previous challenge.

And copy your`.env` file from the previous challenge to this challenge, so you'll be able to run the tests, which will connect to your database.

<br>

# 1️⃣ Ratings table

## 1.1. Create table

Create a table named `ratings` using SQL commands. There are a few requirements based on the data:
- The columns should be named differently than in the CSV (camelCase is not a standard way of naming fields in tables. snake_case is preferred)
    - user_id
    - movie_id
    - rating
    - timestamp
- Choose the correct column types from the list below:
    - `VARCHAR(50)` - when you feel like the length of the data in this field should be limited
    - `TEXT` - when you feel like the length of the data in this field could be big
    - `INT` - if all records in this field seem to be integers that can be stored as 4 bytes (< 2,147,483,647 in absolute term)
    - `BIGINT`- for larger int (8 bytes)
    - `NUMERIC` - if the records may contain decimals
    - `DATE` - self explanatory
- Running the same SQL script again after the table is already created should not fail.

To execute your queries you can either use DBeaver on your local machine, or `psql` from your virtual machines terminal (connect to the `movies` database with `psql movies` 😉)

To explore the structure of the CSV file, you can use bash commands to extract only the first 3 rows (`tldr head`)


🧪 To test that you have created the table correctly, copy the query into `ratings_create.sql` and run `make test`. 1/4 tests should have passed: `test_2.py::test_correct_tables`

## 1.2. Load the data from the CSV in the destination table

- Write down your query in `ratings_copy.sql`.
- 💡 The file path to the CSV should be absolute for dbeaver
- ❗️ It might take a while - the CSV is almost 1GB in size and contains more than 26 million rows

## 1.3. Create a better `timestamp` column

Right now, the timestamp is stored in [epoch time](https://en.wikipedia.org/wiki/Unix_time) format as an `INT` datatype.
We want the date in `TIMESTAMP` to be in a more readable `YYYY-MM-DD HH:MI:SS` format instead!

- Create a new column called `created_at_utc`
- Then, load its converted timestamp equivalent!
- The query should take ~1 minute to run, it's adding an extra field to each ~26 million records!

<details>
  <summary markdown='span'>💡 Hints</summary>

- `ALTER TABLE ... ADD ...` to create a new column
- `UPDATE ... SET ...` to update a column

</details>

🧪 To test that you have correctly updated your table, copy the query into `ratings_update.sql` and run `make test`. 2/4 tests should have passed.

<br>

# 2️⃣ Movies Metadata table

Let's do the same: create & fill a `movies_metadata` table.

👉 Have a quick look at the CSV structure by printing the first two lines to the terminal:

```shell
cat data/movies_metadata.csv | head -n 2
```

There are 24 columns to manually create, each with its own data type!

Thankfully, there exists a useful tool to load CSV's for you.

## 2.1. Create and load automatically with `csvkit`

We have added the utility package [csvkit](https://csvkit.readthedocs.io/en/latest/tutorial/1_getting_started) to your `pyproject.toml`.

Run the following to let csvkit analyse your CSV to automatically create the long `SQL CREATE TABLE` query for you!

```bash
csvsql -i postgresql data/movies_metadata.csv
```

Now that we have the query, we could copy-paste it in dbeaver and load the data like we did for the ratings table... but let's create a `bash script` that automates this for us!

Copy-paste this script in your terminal, we'll explain it below.

```bash
csv_to_postgres () {
    file_path=$(readlink -f $2)
    table_name=$3

    drop_command="DROP TABLE IF EXISTS ${table_name}"
    psql -d $1 -a -c $drop_command

    tmp=$(mktemp)
    csvsql -i postgresql $2 > $tmp
    psql -d $1 -a -f $tmp

    copy_command="\copy ${table_name} FROM '${file_path}' DELIMITER ',' CSV HEADER"
    psql -d $1 -a -c $copy_command
}
```

🔎 **There is a few components to this bash script, so lets break it down!**

It's intended to be run as follows:

```bash
csv_to_postgres movies data/movies_metadata.csv movies_metadata
```
The individual components of the script are:
- `$1` `$2` and `$3` are the arguments passed on the command line
  - `$1` db_name
  - `$2` path_to_csv
  - `$3` table_name

- The first part is stores the table name and file path for later use:
  - `readlink -f $2` provides the absolute file path to our input CSV

- The next part is the drop DB command:
  - A SQL command to drop the table if it exists.
  - Then use `psql -d $1 -a -c $drop_command` to execute the command into our database with `psql`.

- Next, we create the table with our auto generated schema:
  - `tmp=$(mktemp)` creates us a temporary file we can use without having to worry about its cleanup!
  - `csvsql -i postgresql $2` is the most important command. Like when we executed it above, it will generate a schema based on our input csv.
  This command is great on its own, you could use it to generate a schema and work from there to ensure that everything lines up as you expect, but without writing the query manually!
  - We then pipe the output of the previous command to our temporary file `> $tmp`
  - `psql -d $1 -a -f $tmp` is similar to our `psql` command to *drop table if exists*, except that instead of passing a SQL query directly, we are passing a (temporary) file containing a SQL query!

- All that is left to do is copy the data in!
  - Generate a copy command with all the correct variables
  - Execute that into our database `psql -d $1 -a -c $copy_command`

🧪 Execute the command and test that the table was correctly created with `make test` - all tests should be green!

<details>
<summary markdown='span'>💡 That bash function is awesome and I always want it available!</summary>

There is a few ways to have bash functions always available. An easy way is to create a new file in your home directory called `.functions` and then copy the bash function into that file.

```bash
touch ~/.functions
```

Once the file has been created and the function has been saved, add an additional line **at the end** of your `~/.zshrc` file:

```bash
[[ -f "$HOME/.functions" ]] && source "$HOME/.functions"
```

This line will check if the file `~/.functions` exists:
- If the file exists: source the file - this is just your computer reading the file, the same as you typing it into your terminal
- If the file does not exist: stop and skip the `source` step - this prevents crashes if the file doesn't exist

With this line added to your `~/.zshrc`, either run `exec zsh` (this will re-run your `~/.zshrc` file) or close your terminal and re open it (`~/.zshrc` holds your terminal configuration and runs every time you open a terminal) and the bash function will always be available!
</details>

<br>

# 🏁 Finish

In this challenge we set up a database and tables for this unit's challenges, as well as a utility for more easily loading data into a postgres database!

Git add, commit, and push your code so your progress is tracked on Kitt. Then it's time to move onto the next challenge! 🚀

<br>
