# 🎯 Goal

SchemaSpy is a database metadata analyser. It helps database admins and developers visualise, navigate and understand data models and database schemas. SchemaSpy creates a HTML-based report that's easy to use!

<br>

# SchemaSpy

Download SchemaSpy:

```bash
curl -L https://github.com/schemaspy/schemaspy/releases/download/v6.2.4/schemaspy-6.2.4.jar \
    --output schemaspy-6.2.4.jar
```

Make sure your environment variables to connect to the container are available - copy your `.env` from a previous challenge.

Download the driver for postgres:

```bash
wget https://jdbc.postgresql.org/download/postgresql-42.6.0.jar
```

Install graph viz, a package used to create the visualisations:

```bash
sudo apt install graphviz
```

Run SchemaSpy to create the interactive visualisations. There will be a bunch of errors, it's fine. It is because PostgreSQL dropped an obsolete metadata column from version 12 onwards.

```bash
java -jar schemaspy-6.2.4.jar -t pgsql -dp postgresql-42.6.0.jar -db pagila -host 0.0.0.0:5410 -u $POSTGRES_USER -p $POSTGRES_PASSWORD -o output
```

Navigate into the `output` folder, start a webserver, and take some time to explore the docs on `localhost:8000`! The relationship diagrams that SchemaSpy create are particularly useful.

```bash
cd output

python3 -m http.server 8000
```

# In Deployment

One obvious use case is for developers to use it to understand the relationships in a database or warehouse to create new data models. Another is creating documentation for less technical users, but it would need to be easily accessible.

Thinking about SchemaSpy from a DataOps angle:

#### With Continuous Deployment:

You could integrate SchemaSpy into a continuous deployment action to create all the necessary files then dump them into a child repository. Then using another continuous deployment action in the child repository to containerize the web app files and launch a small web app on Cloud Run that has the docs viewable for a given database!

Useful for when you're working with SQL files in version control.

#### With an Orchestrator:

Another implementation could be wrapping SchemaSpy in an API, like FastAPI - all we're doing is running command line arguments to create the output - and a helper function to upload the `output` to a bucket once the output was created.

If we are orchestrating batch loading into a database or warehouse with something like Airflow,
we could use that orchestrator to call that API to create the docs and another process to launch a containerized web app!

Useful for when you doing batch processing in a warehouse.

---

There are lots of different ways to combine different tools to suit your use case. Thinking creatively and putting them together will add value that is greater than the sum of the individual parts.
