# 🎯 Goals and Context

Let's recap what we've done so far. We have built a pipeline that:
- Scrapes data from the front page of [hackernews](https://news.ycombinator.com/front)
- Enforced data quality on the scraped data with great expectations
- Uploads the quality checked data to a data lake

Now we're ready to setup our Data Catalog to really make our data lake more comprehensive and easier to navigate for other stakeholders! We'll be using Google Cloud's Data Catalog so you should be able to reference the boilerplate code in this unit's lecture!

<br>

# 0️⃣ Setup

❓ Copy the `.env` from the previous exercise and add the `PROJECT_ID` variable with the id of your project! You will also need to copy across the GreatExpectations folder `gx` from the previous challenge as well!

<br>

# 1️⃣ Setting up the Entry Group

Create an entry group called `hn_day` in the same location as your bucket!

<details>
<summary markdown='span'>💡 Command if you get stuck</summary>

```bash
gcloud beta data-catalog entry-groups create hn_day --location=eu --description="Entry group for daily Hacker News data"
```

</details>

<br>

# 2️⃣ Creating the Tag Template

Design a tag template to label your data assets. For this challenge, you should have two fields: `source_system` and `source_date`. Representing where the data came from and when it was collected, respectively.

<details>
<summary markdown='span'>💡 Hint</summary>

```bash
gcloud beta data-catalog tag-templates create data_source_info_template --location=eu --display-name="Data Source Info" \
    --field=id=source_system,type=string,display-name="Source System" \
    --field=id=source_date,type=timestamp,display-name="Source Date"
```

</details>

<br>

# 3️⃣ Build the function:

Now you need to implement the `catalog_entry` function in `tag.py`

### 3.1. Initializing the Data Catalog Client:

1. Import the necessary modules to work with Google Cloud's Data Catalog.
2. Initialize a connection to the Data Catalog by creating a client instance.

### 3.2. Setting up the Entry Details:

1. Retrieve the project ID from the environment variables.
2. Specify the location where you're storing the data.
3. Define an entry group for categorizing the data.
4. Generate a unique entry ID, preferably based on the current date.

### 3.3. Configuring the Entry:

1. Initialize a new entry object.
2. Set the display name for the entry, which could be based on the current   date.
3. Provide a description that informs about the data the entry represents.
4. Specify the type of entry you're creating.
5. Configure where the data is located, especially if it's in Google Cloud Storage.

### 3.4. Creating or Retrieving the Entry:

1. Use the client to attempt to create the entry in the Data Catalog.
2. If an entry with the same ID already exists, handle the situation by retrieving the existing entry instead of creating a new one.

### 3.5. Tagging the Entry:

1. Initialize a new tag object.
2. Set the tag template to the one you created earlier.
3. Fill in the tag's fields with appropriate metadata.
4. Attach the tag to the entry using the Data Catalog client.

<br>

# 4️⃣ Testing 🧪:

You can run `python/main.py` and check that your entry gets tagged properly. Feel free to change it to a loop and collect the previous few days of articles to checkout how the catalog would grow!

(There are no unit tests for this challenge!)

<br>

# 🏁 Finish and Conclusion

Congratulations! Now we have a full pipeline: Scraping -> Checking Quality -> Uploading to our lake -> Tagging the data to make it more easily accessible!

Don't forget to push your code to github so Kitt can track your progress!

<br>
