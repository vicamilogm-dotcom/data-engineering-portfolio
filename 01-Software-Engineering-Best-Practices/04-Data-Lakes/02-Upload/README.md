# 🎯 Goals

The goal for this exercise is to integrate the scraping process you've previously set up with a data upload mechanism. As a data engineer, being able to write code that interacts with cloud services is an integral skill.

After scraping stories from [Hacker News](https://news.ycombinator.com/news), you will upload them to a Google Cloud Platform (GCP) bucket, organizing the data within a data lakes raw zone.

<br>

# 0️⃣ Setup environment variables

1. Create a `.env` by renaming the `.env.sample` file
2. Populate the `.env` with a bucket name. You might need to get creative because the bucket will need to be globally unique!

<br>

# 1️⃣ Create a GCP Bucket

1. Create a bucket in GCP with the name that is stored in `$LAKE_BUCKET`. In production, if latency is important, you would choose the region closest to you for optimal performance.
2. Once the bucket is set up, verify its creation by running the test: `pytest tests/test_upload.py::test_bucket_exists`

<details>
<summary markdown='span'>💡 Hint</summary>

To create a bucket in GCP, navigate to the GCS section in the GCP console. Click on "Create Bucket", choose a unique name, and select the region closest to you. Or with gcloud:

```bash
gsutil mb -l eu gs://$LAKE_BUCKET
```
</details>

<br>

# 2️⃣ Upload to GCP

Familiarize yourself with the `upload_to_lake` function in the `upload.py` file - try to understand what is happening at each line! Once you're familiar with the function:

- Modify the function (if necessary) to upload the CSV file to your GCP bucket. We're organizing data in the data lake's raw zone using a date-based structure (as seen in the lecture).
- Ensure you set up authentication with GCP to allow file uploads.

<details>
<summary markdown='span'>💡 Hint</summary>

If the permissions are not working, run the following and follow the instructions:

```bash
gcloud auth application-default login
```
This command sets an environment variable that will use the permissions attached to your personal email principal on your GCP account. If you want, try to modify the code to see if you can get authentication from the service account you created on Set Up Day! You'll have to modify the storage client instantiation.
</details>

<br>

# 3️⃣ Putting it all together

We can now run the first two parts of our pipeline together that will:
- Scrape the front page of [hackernews](https://news.ycombinator.com/front)
- Upload the data as a CSV to our GCP bucket

After running your integrated script, `main.py`, ensure that the data is both scraped and uploaded to the GCP bucket by viewing the bucket through the [console](https://console.cloud.google.com/storage/browser)!

<br>

# 🏁 Finishing up

🧪 Once you've confirmed that the data exists in your bucket, execute `make test` to run the tests that will verify your code and organization of the uploaded data within your data lake.

Congratulations on completing the exercise! You've successfully integrated your scraping process with a data upload mechanism, uploading the scraped data to a data lake's raw zone. Now we are ready to integrate data quality checking 🚀

Don't forget to push your code to github so Kitt can track your progress!

<br>
