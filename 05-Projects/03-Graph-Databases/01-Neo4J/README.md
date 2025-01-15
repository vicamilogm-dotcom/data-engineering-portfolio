# 🎯 Goal

This is short exercise to run a local instance of the Neo4j database using Docker Compose, and do Neo4j's official [movie graph tutorial](https://neo4j.com/developer/cypher/guide-cypher-basics/#cypher-movie-find). By the end, you'll be familiar with the power of graph databases for highly connected data, and how non-SQL query languages can help express graph / tree 🌳 patterns.

<br>

# 1️⃣ Run Neo4j in Docker Compose

Based on:
- How we ran Postgres in previous days and exercises.
- Neo4j's recommendations on [how to run their Docker image locally](https://neo4j.com/developer/docker/), which should give you hints on the used ports and environment variables. Use the following image: `neo4j:4.2.18-community`.


**❓Write a `docker-compose.yml` file to mimic what this Docker command does.**

💡 Why bother with docker-compose when we can use a simple docker run? Saving setup instructions explicitly in a yml file is much easier than remembering the docker command by heart. You'll be happy to find such "ready to work" template challenges later on!

<details>
<summary markdown='span'>💡 Hints</summary>

- To connect, type `neo4j` as the username and `s3cr3t` as the password, that's how we interpret their `NEO4J_AUTH=neo4j/s3cr3t` environment variable
- 💯 Did you create a `.env` file to store the `NEO4J_AUTH` environment variable value? Or did you hardcode it in the `docker-compose.yml` 😡. If the latter, modify your `docker-compose.yml` file and create a `.env` file based on the template from the `env-template`!
- Do not forget to also open port 7687 ❗ This port handles the communication between the database and Neo4j, and handles the database connection among other things.

</details>

🧪 Docker compose up the service, make sure you understand the logs, then open up [http://localhost:7474/browser/](http://localhost:7474/browser/) in your browser, does it work?

<br>

# 2️⃣ Play with Movies dataset

Type `:play movie graph` 🎥 and be guided directly in the browser! 💻

<br>

# 3️⃣ More Neo4j please! (Optional)

This tutorial about building a recommendation engine [at this link](https://neo4j.com/developer/cypher/guide-build-a-recommendation-engine/) comes next for the bravest 😱.

<br>
