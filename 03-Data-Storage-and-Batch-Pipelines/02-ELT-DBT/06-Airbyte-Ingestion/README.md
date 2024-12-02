# 🎯 Goal

This is an optional challenge. There is already a number of challenges to complete today. But we wanted to provide a challenge on how to get Airbyte up and running to ingest data from a GCP Cloud Storage Bucket and load into BigQuery. You could use this challenge as a reference for your final project, and it is also suitable for small deployments on an adequately sized stand alone VM.

## Context

The Marketing team has heard of the fantastic work you did for the Finance team and want you to automate the loading of their raw data from Google Cloud Storage into BigQuery for their analysts to work with.

The marketing team run ad campaigns on four platforms:
- Adwords
- Bing
- Criteo
- Facebook

You know that the marketing team place their data into a GCS Bucket as **parquet** files for archiving every week.

Airbyte is a great tool to manage the ingestion of the data from a GCS Bucket to BigQuery, and even has some built in basic automation. Let's see how we could set it up.

It's worth mentioning that Airbyte has fantastic documentation, and was designed to be as user friendly as possible. If you get stuck on creating sources, destinations, or connectors, checking the official documentation should be the first thing you do!

<br>

# 1️⃣ Download and Stage Data

In the case study, the marketing team put their data into a GCS Bucket every week for archiving. We'll have to imitate this by downloading the data and uploading it to our own bucket.

Download raw marketing data:

```bash
mkdir -p data/marketing/

curl -o ./data/marketing/raw_gz_adwords.parquet https://wagon-public-datasets.s3.amazonaws.com/data-engineering/gz_raw_data-raw_gz_adwords.parquet
curl -o ./data/marketing/raw_gz_bing.parquet https://wagon-public-datasets.s3.amazonaws.com/data-engineering/gz_raw_data-raw_gz_bing.parquet
curl -o ./data/marketing/raw_gz_criteo.parquet https://wagon-public-datasets.s3.amazonaws.com/data-engineering/gz_raw_data-raw_gz_criteo.parquet
curl -o ./data/marketing/raw_gz_facebook.parquet https://wagon-public-datasets.s3.amazonaws.com/data-engineering/gz_raw_data-raw_gz_facebook.parquet
```

Create a bucket named: `<your_github_username>-greenweez-raw`. Remember the name has to be globally unique!

```bash
gsutil mb -l EU gs://<your_github_username>-greenweez-raw
```

Move downloaded files to your bucket:

```bash
gsutil cp data/marketing/* gs://<your_github_username>-greenweez-raw/greenweez/raw/marketing/ad-campaigns/
```

Have a look on the [Google GCS console](https://console.cloud.google.com/storage/browser) to confirm that your files are in your bucket! Pay attention to the path of the files and think about why we have created such an explicit path.

<br>

# 2️⃣ Download, Install, and Run Airbyte

[Airbyte OSS (Open Source Software)](https://docs.airbyte.com/using-airbyte/getting-started/oss-quickstart) uses a Kubernetes deployment - don't worry, you do not need any Kubernetes knowledge for now! Airbyte has created a command line utility called: **abctl**, that abstracts a lot of the Kubernetes aspects away.

To download and install **abctl**, run the following in your terminal:

```bash
curl -LsfS https://get.airbyte.com | bash -
```

Once **abctl** has downloaded and installed, start Airbyte with:

```bash
abctl local install
```

This will create a local Kubernetes cluster. It might take a few minutes to pull the relevant images and spin up the cluster.

Once the installation is complete, your should see a message saying that: A password may be required to login. The password can be found by running the command `abctl local credentials`. Obtain your credentials by running the above command in your terminal:

```bash
abctl local credentials
```

Copy your password, we'll need it in a second.

And you should see a message saying that the your entrypoint is available on **http://localhost:8000** Make sure that VS Code has forwarded port 8000 and open it in your browser.

In your browser, enter your email and a company name (anything will do). Click **Get started** and on the next page, paste in your password from `abctl local credentials` and click **Log in**.

We're nearly ready to create our first connector!

<br>

# 3️⃣ Sources and Destinations

Airbyte works on the principle of **sources**, **destinations**, and **connections**.
- A **source** is where the data is sourced, or ingested from
- A **destination** is where the data is loaded to
- A **connection** links a **source** and a **destination** to form a pipeline

We need to have at least one source and one destination before we can connect them together. But before that we need credentials so Airbyte can access cloud services to read and write data.

## 3.1. Service Accounts

Airbyte uses Service Accounts and Service Account JSON keys to authenticate with cloud services it's retrieving and loading data from. It's up to us to create the service accounts and manage access. Depending on the size and data maturity of a company, managing IAM may be done at a higher level or by a dedicated team.

You could use our previously created Service Account that was created at the start of the bootcamp, but it has very far reaching permissions, and a large attack surface. If our Airbyte deployment was compromised by a bad actor, the bad actor could do almost anything they wanted to on your GCP Project.

Let's create two new service accounts and service account keys with the minimum required permissions. One for GCS (source) and one for BigQuery (destination).

## 3.1.1. GCS Service Account and Key

Navigate to the [Service Accounts tab](https://console.cloud.google.com/iam-admin/serviceaccounts) of IAM & Admin on the GCP Console.
- Click **Create Service Account** at the top of the page
- Give your service account a name. It's best practice to name a service account after it's function. Name it: **airbyte-greenweez-gcs**
- Give the service account a description
- Click **Create and continue**
- Give the service account the role(s):
    - **Storage Object Viewer**
    - **Storage Object User**
- Click **Done** at the bottom of the page
- On the Service Accounts page, click on the email address of the service account that you just created.
- Select the **Keys** tab at the top of the page
- Click **Add Key**, then **Create new key** from the drop down list
- On the pop up tab, make sure that **JSON** is selected, then click **Create**
- Your key should have downloaded to your local computer, keep it safe for now. Give the key a more explicit name if you can: `de-bootcamp-airbyte-greenweez-gcs.json`

You will need some additional legacy permissions for your GCS Service Account, let's configure them now:
- Navigate to your bucket in the [GCP Console](https://console.cloud.google.com/storage/browser). You can search for Cloud Storage in the top search bar on the console.
- Select your bucket created for **<your_github_username>-greenweez-raw**
- Select the **Permissions** tab
- Scroll down and click on **Grant Access**
- In the pop up window, start typing your Service Account name: airbyte-greenweez-gcs, and you shuold be able to select the service account.
- Under the **Assign roles** section, select **Storage Legacy Bucket Reader** from the drop down menu.
- Click **Save**

Your GCP Cloud Storage Service Account is now set up and ready to go 🎉

Let's create one for BigQuery!

## 3.1.2. BigQuery Service Account and Key

Navigate to the [Service Accounts tab](https://console.cloud.google.com/iam-admin/serviceaccounts) of IAM & Admin on the GCP Console.
- Click **Create Service Account** at the top of the page
- Give your service account a name. It's best practice to name a service account after it's function. Name it: **airbyte-greenweez-bigquery**
- Give the service account a description
- Click **Create and continue**
- Give the service account the role(s):
    - **BigQuery User**
    - **BigQuery Data Editor**
- Click **Done** at the bottom of the page
- On the Service Accounts page, click on the email address of the service account that you just created.
- Select the **Keys** tab at the top of the page
- Click **Add Key**, then **Create new key** from the drop down list
- On the pop up tab, make sure that **JSON** is selected, then click **Create**
- Your key should have downloaded to your local computer, keep it safe for now. Give the key a more explicit name if you can: `de-bootcamp-airbyte-greenweez-bigquery.json`

And now your BigQuery Service Account should be good to go now!

## 3.2. GCS Source

Let's start with creating a source to read from our GCS Bucket.

Click on either **Create your first connection** on the welcome screen, or **Sources** in the left hand menu.

- Take a minute to look through all the sources that Airbyte has. When you're ready, in the search bar at the top of the screen, type **GCS**. If you can't immediately see a source for Google Cloud Storage (GCS), try the **Marketplace** tab.
- **Name**: GCS Greenweez Ad Campaigns
- **Service Account Information**: Paste the *entire contents* of your `de-bootcamp-airbyte-greenweez-gcs.json` into the box
- **Bucket**: the name of your bucket, it should be **<your_github_username>-greenweez-raw**
- On the list of streams to sync, click add. Each stream corresponds to a different schema, or table that will be created in BigQuery. We have four separate tables, so we will need four different streams. Give each stream the following parameters:
    - **Parquet Format** - easy to miss!
    - **Name** - what the output table in BigQuery will be named. Follow the convention of: `raw_gz_<company>` where company is where the ad campaign was run. For **bing** it would be: **raw_gz_bing**
    - **Globs** - the files that correspond to the stream (or table), in [glob format](https://en.wikipedia.org/wiki/Glob_(programming)). It will need to match the name of the file, and path for the raw files in your GCS bucket.
    - Make sure create a new stream for each platform ads campaigns were run on.
    - **Input Schema** and **Files to Read for Schema Discover** are not required
    - When you have completed all streams, click **Set up source** at the bottom of the page.

<details>
<summary markdown='span'>💡 Glob Hint</summary>

For glob paths you can make use of the wildcard character: `*`

Depending on how explicit you want to be, you could use:
```bash
**/ad-campaigns/*<company_name>.parquet
# e.g. bing would be: **/ad-campaigns/*bing.parquet
```

Or if you really wanted to be specific about raw marketing ad-campaign data use something like:

```bash
**raw/marketing/ad-campaigns/*<company_name>.parquet
# e.g. bing would be: **raw/marketing/ad-campaigns/*bing.parquet
```
</details>

If your service account and the source config is correct, the source connector should have been created!

## 3.3. BigQuery Destination

Let's create our BigQuery destination. Select **Destinations** from the left side menu, or search for BigQuery in the **search bar** at the top of the Destinations screen.

On the next screen fill out the following parameters:
- **Destination Name**: BigQuery Greenweez Raw Data
- **Project ID**: Your GCP Project ID
- **Dataset Location**: You can select **EU**
- **Default Dataset ID**: This is the BigQuery Dataset to load data into - it should be: **raw_gz_data**
- **Loading Method**: Choose Batched Standard Inserts
- **Service Account Key JSON**: Paste the *entire contents* of your `de-bootcamp-airbyte-greenweez-bigquery.json` into the box

If your service account and the destination config is correct, the destination connector should have been created!

Congrats! You should now have a source and a destination, let's put the two together and create a connection!

<br>

# 4️⃣ Create a Connection

Navigate to the **Connections** tab from the left hand side menu and click on **Create your first connection**. We'll have to work through four tabs to set up the connection.
- **Define source**: Select your GCS source from the list.
- **Define destination**: Select your BigQuery destination from the list.
- **Select Streams**:
    - Might take a minute to load, Airbyte needs to fetch schema information
    - Select all the streams to sync with the toggle next to each stream
    - Airbyte might be unhappy that you don't have a primary key defined for the default sync mode: **Incremental | Append + Deduped**. Change the Sync mode for each stream to: **Full refresh | Overwrite**. Read more below for different sync modes.
    - If you click on a stream, you can see the schema and select a primary key or cursor field depending on the sync mode
    - Click **Next**
- **Configure connection**:
    - **Connection Name**: You can give your connection a more explicit name if you wish
    - **Schedule Type**: Airbyte offers three different scheduling options:
        - Manual: No scheduling at all - you'd use this for external orchestration, like Airflow.
        - Scheduled: Options of every 1, 2, 3, 6, 8, 12, or 24 hours. Select this for every 24 hours.
        - Cron: Cron scheduling and syntax - more granular than the Scheduled option.
    - **Destination Namespace**: Destination-defined is fine for our use case.
    - **Stream Prefix**: Can leave it blank. But for example, we could have named our streams in our GCS source as just: **adwords**, **bing**, **criteo**, **facebook** and then added a prefix here with **raw_gz_** for the same outcome.
    - Feel free to look in **Advanced settings**, when you are ready click **Set up connection**

Your Airbyte connection should start syncing your data! You can check the status for each stream in the **Status** tab. If you want to find logs for a specific run, select the **Timeline** tab, select the **kebab menu** for a run, then **View logs** from the drop down menu.

When you are done, have a look at the data on BigQuery! Do you notice anything about the tables that have been loaded in from Airbyte? Airbyte has added some metadata columns that it uses internally.

💡 Different sync modes are specific to the data you have and problem you are trying to solve. You can save computation and time if you select a sync mode that suits your data. Find out more on the official docs at [this link](https://docs.airbyte.com/using-airbyte/core-concepts/sync-modes/)

<br>

# 🏁 Finishing up

We have gone through setting up a GCP source and BigQuery destination in Airbyte, as well as creating the required permissions.

We have set things up primarily through the GUI, but you can apply settings programmatically for more fine grained control, or for more automation.

If you wanted to take Airbyte further, check out the [quickstart at this link](https://docs.airbyte.com/using-airbyte/getting-started/oss-quickstart#using-an-ec2-instance-with-abctl). The quickstart has some common customizations including:
- Using an External Database for metadata
- State and Logging Storage
- Secret Management

There are no tests for this challenge.

## Teardown

Make sure to teardown your Airbyte cluster so it isn't using system resources when it's not necessary.

To teardown your Airbyte cluster **while preserving any data you have created**:

```bash
abctl local uninstall
```

To teardown your Airbyte cluster and **purge any persistent data**:

```bash
abctl local uninstall --persisted

# And clear out any remaining data

rm -rf ~/.airbyte/abctl
```

<br>
