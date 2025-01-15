# 🎯 Goal

The goal of this exercise is to put our API into production with a managed Cloud SQL database{}

We will:
- Create a production database, a managed SQL instance on GCP [Cloud SQL](https://cloud.google.com/sql), to hold our user, tweet, and like data.
- Put our **Twitter API** running in a container in the cloud on [Google Cloud Run](https://cloud.google.com/run).
- Accessing our **production database** to verify that everything is working!

We have provided the solution to the `twitter_api` package as well as the associated `alembic` migration you previously built as a starting point.

### 🚨 🚨 Cost Alert 🚨 🚨

We are going to create a **Cloud SQL** instance. Cloud SQL instances come with many benefits (fully managed, backup and disaster recovery, security, integrates easily with other GCP Services), but they have a cost to match the convenience. **Cloud SQL** instances are inherently Virtual Machines that can't be "paused".

A Cloud SQL instance in `europe-west1` in the default configuration in early 2025 with:
- 8 vCPU's = $0.33 / hour
- 32 GiB RAM = $0.22 / hour
- 250 GiB SSD = $0.0.6 / hour
- A high availability VM = $0.61 / hour

**Total = $1.23 / hour OR ~$30 / day** 💸

This challenge shouldn't take you long, about an hour. So it shouldn't cost more than ~$1.50 or ~€1.50

❗ **If you start this challenge but do not finish it, it is super important that you tear down the instance!** ❗

You can manage your Cloud SQL instances from the Cloud SQL GCP console at [this link here](https://console.cloud.google.com/sql/instances).

<br>

# 1️⃣ Setup a Google Cloud SQL instance

First, copy the `.env.sample` into a new `.env`. You will notice we have a few extra environment variables than our original twitter app! Fill:
- `POSTGRES_PASSWORD` with the password you want.
- `LOCATION` where your VM is located (e.g. europe-west1)

Go to [gcp console UI - SQL section at this link here](https://console.cloud.google.com/sql/choose-instance-engine), and create a database instance with the following properties:
- Enterprise
- **instanceID**=twitter-prod
- **root-password**=<your_postgres_password> - the value of `POSTGRES_PASSWORD` in your `.env`
- **database-version**=POSTGRES_14
- **region**=<your_region> - the value of `LOCATION` in your `.env`
- **connections:**
    - Private IP
    - Default network
    - Allocated IP range: Use the automatically assigned IP range

<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W0D5/cloudSQL.png" width=500>

**About networks ☝️**

- Here, we tell the GCP not to assign any public IP address to our database: there is no need for anyone external to be able to access the database directly except through the API. This way, even if we somehow leak our password, no-one will be able to connect without breaking into our GCP first 🔐

- We picked the "default" option because it is the same network as all your other GCP projects services, which include your beloved VM. We could have created a separate private network just for the app if we wanted even more isolation!

<br>

# 2️⃣ Setup the tables

## 2.1. Connection

Let's connect! **We need the private IP** of our SQL instance so we can run it, and so the DB isn't accessible through a public internet's IP address.

```bash
gcloud sql instances describe twitter-prod | grep ipAddress
```

And now you have the IP address to populate into your `.env`! Don't forget to `direnv reload`.

Connect with `psql` via the default "postgres" user and DB:

```bash
psql "hostaddr=$POSTGRES_IP port=5432 user=postgres dbname=postgres password=$POSTGRES_PASSWORD"
```
☝️ We used the string syntax instead of the usual `psql --host=$POSTGRES_IP --port=...`

🎉 You are now inside the newly created cloud SQL instance
- Connecting via DBeaver from our local machine is not as easy because the managed Cloud SQL instance is outside our Google Projects' virtual private network, where your VM is inside it.
- Hopefully, `psql` should be sufficient to verify the creation of our tables!

## 2.2. Database creation

If we try to create our database in `psql`, it won't work. For **Cloud SQL**, we have to create our database via the `gcloud` CLI tool. To create a `twitter-prod-db` database on your `twitter-prod` Cloud SQL instance, run the following command:

```bash
gcloud sql databases create twitter-prod-db --instance=twitter-prod
```

Add this new DB name `twitter-prod-db` to your `.env` at `$POSTGRES_DATABASE_NAME`

## 2.3. Table creation

Now, we have our `twitter-prod-db` database in our `twitter-prod` postgres instance! **We can use alembic to create the yesterday's tables directly onto our new cloud SQL instance.**. We already have a revision history (the revisions will also populate a few rows in each table), and a populated `alembic/env.py` file. So alembic knows to connect to your `$POSTGRES_DATABASE_URL` (line:23)

❓ Now apply the migration to the database and connect and check with `psql` that your database looks the way you would expect.

<details>
<summary markdown='span'>🎁 Solution</summary>

Simply run:
```bash
alembic upgrade head
```
</details>

❗️ Now you should see how alembic helps you to keep track of all your migration files. Being able to replicate our previous local `dev` environment to our `prod` database is super powerful!

<br>

# 3️⃣ Containerize API

🎯 We want to be able to call our Twitter API from our local machines web browser --> through our VM --> through our container running on your VM --> reading or writing to Google Cloud SQL!

Before we get started on the `Dockerfile`, we need to complete our `POSTGRES_DATABASE_URL` in our `.env`. Unfortunately Docker can't read environment variables built from other environment variables when passed at runtime (a process called parameter interpolation). So we need to hardcode the `POSTGRES_DATABASE_URL`. Docker Compose does support parameter interpolation, but you'll have to wait for the next module to see 😉

❓ Complete the `POSTGRES_DATABASE_URL` in your `.env`. Don't forget to `direnv reload`!

❓Create a new `Dockerfile` and bring the code over.
- You have a great re-usable framework for a Docker image from the previous challenges if you need inspiration.
- The image needs to build from the challenge root folder
```bash
docker build --tag=twitter .
```
- And the container should run well too, launching out API with uvicorn, listening on port 8000 on your localhost, and exposing the port 8000 to your local machine too!
```bash
docker run twitter
```

❗️ You may see an error: This is because in your container (and contrary to your VM), the `.envrc` is not activating and therefore not loading the `.env` file into shell ENV variables. We could install direnv in the container, but it makes more sense to use Docker to populate the environment only at run time:

```bash
docker run --env-file=.env twitter
```

☝️ Now that we are populating the environment at run time, we don't need the `.env` to be copied into the container, nor do we want it to be there for security reasons

Here is where the concept of a `.Dockerignore` file becomes useful (it functions like a `.gitignore`). For example, create one with the following, and rebuild, and re-run the container. If you attached a shell to the container, you should see no `.env` files, yet its environment variables will still be available!

```bash
alembic
.env
.env.sample
.envrc
.alembic.ini
.README.md
```
☝️ Always try to keep your image as lean as possible

Now, let's publish the port to make our API available

```bash
docker run --env-file=.env -p 8010:8000 twitter
```

We are mapping 8010 on our VM to 8000 inside the container. If we forward the port to our host machine, we can now check out our running Twitter app. When all looks good, try an endpoint.

Amazing, we are now plugged into our hosted database! Let's go one step further and run our API on Cloud Run.

🎉 **You should be able to read the list of all tweets by calling `GET /tweets` from your local machine's chrome app --> through your VM --> through your container --> to Google cloud SQL!**

<br>

# 4️⃣ Put your app in production through Google Cloud Run

🎯 Final step - we want to get rid of our VM entirely and run our app on Google Cloud Run!

🎯 We want to call our Twitter API from our local machines web browser --> pinging our container on Google Cloud Run --> updating or reading from Google Cloud SQL!

## 4.1. Push to Cloud Run

First, let's populate our related values in our `.env` file:

```bash
LOCATION=<USE_SAME_ZONE_AS_YOUR_G_CLOUD_SQL>
HOSTNAME=$LOCATION-docker.pkg.dev
PROJECT_ID=<INSERT_YOUR_GCP_PROJECT_ID>
REPOSITORY=docker-hub
IMAGE_NAME=twitter
IMAGE_TAG=prod
IMAGE_FULL_TAG=$HOSTNAME/$PROJECT_ID/$REPOSITORY/$IMAGE_NAME:$IMAGE_TAG
```

❓ Now, tag and push our image on Cloud Run

<details>
<summary markdown='span'>🎁 Solution</summary>

```bash
docker tag twitter $IMAGE_FULL_TAG
docker push $IMAGE_FULL_TAG
```
</details>

## 4.2. Create a Virtual Private Connection (VPC)

Now comes one additional complexity: we need to create a VPC connector to describe to the Cloud Run where to route the internal traffic.
So far, our VM has been in the same VPC as your GCloud SQL, but it's different for Cloud Run:

Here is the gcloud command below to create a VPC named "twitter-connector":

```bash
gcloud compute networks vpc-access connectors create twitter-connector \
    --region=europe-west1 \
    --range=10.9.0.0/28 # CIDR range of internal addresses that are reserved for this connector.
```
## 4.3. Deploy on Cloud Run

📚 Take a minute to read the [docs](https://cloud.google.com/run/docs/deploying)

You should see a couple of extra arguments from the lecture we'll have to use:

- `add-cloudsql-instances`: Speaks by itself!
- `vpc-connector`: Needed when our cloudsql instance is on a Private IP network as we have [docs](https://cloud.google.com/sql/docs/mysql/connect-run?authuser=1#private-ip)
- `allow-unauthenticated`: We want our Twitter API to be publicly available (just for this challenge)
- `set-env-vars`: We need to pass the same env variable as when locally running Docker. However, gcloud does not accept "--env-file=.env" syntax, so we can either pass each variable manually or create a yml with env variable. We decided to pass the required variables manually.


```bash
gcloud run deploy twitter-prod \
    --image $IMAGE_FULL_TAG \
    --vpc-connector=twitter-connector \
    --region=europe-west1 \
    --add-cloudsql-instances=twitter-prod \
    --allow-unauthenticated \
    --set-env-vars POSTGRES_DATABASE_URL=$POSTGRES_DATABASE_URL
```

For the region, we put Cloud Run and the database in the same region to minimise latency!

❗️ **This still won't work: Try to see if you can spot the error message:**

> _The user-provided container failed to start and listen on the port defined provided by the PORT=8080 environment variable_

<details>
<summary markdown='span'>💡 Hint to the failure</summary>

Cloud Run needs our API to start on the `$PORT`, a special env variable that will be injected by Cloud Run at runtime. You need to update your Dockerfile with `$PORT` instead of hard-coding the port number.
</details>

🏁 Once you have fixed everything locally, push and re-run the deploy command. You should be able to access your API managed by Cloud Run connected to your managed database!

<br>

# 🏁 Finishing up and Teardown

Managed SQL instances are essentially running on VM that is up all the time with some extra features rolled in, and they have a cost to match 💸 Make sure that you pull down your Cloud SQL instance.

Go to [console.cloud.google.com at this link](console.cloud.google.com) and shutdown the following services using the web user interface:
- Your Cloud Run twitter-prod instance
- Your Cloud SQL twitter-prod database
- Your [VPC](https://console.cloud.google.com/networking/connectors/) twitter-connector

<br>
