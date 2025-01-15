# 🎯 Goal

<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W2D2-nosql/mongodb.png" alt="drawing" width="200"/>

The goal of this session is to get familiar with **MongoDB**, a document database. The challenges are structured as follows:
- We will start with **setting up** the MongoDB services using `docker-compose`
- We will then get you up to speed with the **syntax** of MongoDB and its **functionalities**.
- The advanced exercise is more open, and focuses on interacting with MongoDB using the Python package `pymongo`, which would likely be the way in which you would interact with the database in a **production environment**.

<br>

# 1️⃣ Set up

We will use 2 different images, one from `Mongo` and one from `Mongo Express`, which is an interactive lightweight Web-Based Administrative Tool 💻  to interact with the MongoDB Databases through the UI.

## 1.1. MongoDB service

❓ Add a new service named `mongo` with the following properties. Reference the dockerhub readme at [this link](https://hub.docker.com/_/mongo) to check the syntax:
- `image`: specify the name of the Docker image to use for the MongoDB instance and use version `6.0`
- `restart`: `always`
- `environment`:
  - specify the desired username and password for the MongoDB root user
- `volumes`:
  - specify the host directory `data/db` where you want to store the MongoDB data files and the corresponding directory `data/db` in the Docker container
- `ports`:
  - specify the host port and the container port that you want to use for accessing the MongoDB instance - use `27017`


☝️ This will create a Docker container for the MongoDB instance using the specified Docker image.

💡 The `restart` property specifies that the container should always be restarted if it stops. The `environment` section specifies the username and password for the MongoDB root user. The `volumes` section mounts the local directory where you want to store the MongoDB data files to the corresponding directory in the container. The `ports` section forwards the local port and the container port that you specified, allowing you to locally connect to the MongoDB instance.

## 1.2. MongoDB Express service

❓ In the `docker-compose.yml` file, add a new service named `mongo-express` with the following properties (use the [mongo-express-docker documentation at this link](https://github.com/mongo-express/mongo-express-docker#configuration))
- `image`: specify the name of the Docker image to use for the MongoDB Express web interface and use version `1.0.0-alpha`
- `restart`: `always`
- `ports`: specify the host port and the container port that you want to use for accessing the `mongo-express` web interface - use `8081`
- `environment`:
  - specify the username and password for the MongoDB root user
  - specify the URL of the MongoDB instance in the following format `mongodb://<username>:<password>@<host>:<port>/`
- `depends_on`: the express service depends on the mongo service, make that explicit

## 1.3. Get it up and running

❓ Run:
```bash
docker compose up
```

And visit `http://localhost:8081` after initialization to check it out!

💡 The `docker exec` command allows you to run commands inside a Docker container. This allows us to interact with MongoDB inside the container.

❓ Run the following command to create a bash shell inside your mongo container:

```bash
docker exec -it [CONTAINER NAME] /bin/bash
```

<details>
<summary markdown='span'>💡 Hint</summary>

💡 Use the container name of the mongo service, not of the mongo-express service. You want to interact with the database, not with the UI!
</details>


❓ Run `mongosh` inside the container to interact with Mongo using your username and password. Replace the values with the credentials that you used in the docker-compose file.
```bash
mongosh admin -u username -p password
```

🚀 You are now ready to interact with the database. You can run `help` to see which commands are available

<br>

# 2️⃣ MongoDB Basics

📚 First, take 5 min to scroll through the official [MongoDB vs. SQL comparison](https://www.mongodb.com/docs/manual/reference/sql-comparison/) tutorial!

<img src="https://www.mongodb.com/docs/manual/images/crud-annotated-mongodb-insertOne.bakedsvg.svg" width=400>

👉 Your turn!

**❓ Switch a database "food" (that doesn't exist yet)**

```bash
use food
```

**❓ Create a collection 📁**

```bash
db.createCollection("fruits")
```

- ✅ Verify in the CLI that database has been created.
- ✅ Verify also `Mongo-express` that the database has been created.

For the following questions, use the [documentation of MongoDB](https://www.mongodb.com/docs/manual/reference/method/) to find the right method to use per question.

<details>
<summary markdown='span'>💡 Need help?</summary>

💡 The answers can be found in the README of the answers subdirectory. But only use this as your last resort!
</details>

**❓ Insert the following list of documents into the fruits collection 📄**
```bash
[
  {name: "apple", origin: "usa", price: 5},
  {name: "orange", origin: "italy", price: 3},
  {name: "orange", origin: "florida", price: 4},
  {name: "mango", origin: "malaysia", price: 3}
]
```

**❓ Find the all documents from the fruits collection**
- Find only the oranges
- Try to do the same from mongo express UI with the Simple, then Advanced interface
- Find only one specific item by its ID

💡 What happens when you try to query an item that does not exist in the db ?

Finally, take 3 min to read the MongoDB Query Documents docs at [this link here](https://www.mongodb.com/docs/manual/tutorial/query-documents/).

**❓ Insert another record, but now also containing the color.** 💡 this is no problem for Mongodb due to it being **schemaless**
```bash
{ name: "apple", origin: "usa", price: 3, color: "red" }
```

**❓ Update** the record you just inserted ☝️ by increasing its price to 4

**❓ Count** the number of *documents* in the collection
- 💡 What happens when you try to query a country that does not exist in the db, e.g. `FRA`?

**❓ Delete** all the fruits that are from Italy

**❓ Drop** the entire collection 💥

👊 These exercises should have given you a good idea of some of the common operations that you can perform with MongoDB. It is time to work in a more production-ready environment!

<br>

# 3️⃣ PyMongo

## 3.1 Setting up the db connection in Python

We will use the `pymongo` library to interact with the MongoDB database from Python 🐍.  The commands will be very similar, but by including in Python scripts we can structure our code better. There is already an outline of the functions that will need to be written, it is your job to create the logic for these functions 💪.

❓ Lets start by setting up the database connection in `app/pymongo_get_database.py`.
- Try to get the command: `python -m app.pymongo_get_database` to run successfully

<details>
<summary markdown='span'>💡 Hints</summary>

Load correct username and password from the `.env` file (see `.env.sample` for the syntax) and use them in the connection string (instead of hardcoding) them. By loading them from a `.env` file and including that file in `.gitignore`, you are making sure to not store any credentials in `Git` 💀. The function `get_database` allows you to interact with the `restaurant` database, as specified in the return variable of the function.

`Client['restaurant']`? The MongoClient class has a dictionary-like interface for accessing databases, which allows you to use the square brackets (`[]`) to access a specific database. In this case, the code is accessing the restaurant database by using client['restaurant']. If the restaurant database does not already exist, PyMongo will create it when it is first accessed.
</details>

🚀 Nice, you have set up the database connection using 🐍 and created a database called `restaurant`! We are now going to ingest documents into this database

## 3.2. Inserting the documents

❓ Open `ingest.py` and follow instructions!
- The script should run with: `python -m app.ingest`
- What happens when you run the `ingest_data` file multiple times?
- You can also check in mongo express whether the documents have been successfully inserted.

## 3.3. Reading data

We are now ready to read the data from the database using python!
Good new, `pymongo` query syntax is extremely similar than that of `mongosh`.

❓ Work in the `app/query.py` file
- 🧪 Test it step by step with `python -m app.query` to understand how pymongo works!
- 💡 We advise you to set interactive breakpoints in your code or to use interactive session (ie, notebooks) to learn the pymongo syntax step by step!

<br>

# 🏁 Finishing up

Congratulation on finishing these MongoDB exercises! You should now have a grasp on how document databases work and how to implement them in your own projects! 🚀

🧪 Test all your code with:

```bash
# Make sure your docker compose stack is running!
make test
```

And don't forget to git add, commit, and push your code to Github!

<br>
