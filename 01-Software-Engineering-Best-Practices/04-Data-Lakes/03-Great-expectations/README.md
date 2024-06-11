# 🎯 Goals

With the data scraped and uploaded, we want to ensure data quality in our data lake so it doesn't turn into a data swamp!

Your primary task in this exercise is to complete the `run_expectations` function within the `expectations.py` file. This function will harness the power of Great Expectations to validate the quality of a given DataFrame.

Typically, once you set up quality checks you would either stop the pipeline or add reporting. In our case, because we are scraping, we don't want to delete the data we have already scraped, but will notify a channel about when it fails!

<br>

# 0️⃣ Setup:

Intilaize great expectations

```bash
great_expectations init
```

This will create all of the files needed to manage our expectations!

❗ Duplicate your `.env` from the previous exercise and copy across the `stories.csv` - we'll need them both!

<br>

# 1️⃣ Understanding the Context:

Before you delve into writing the code, you need to grasp the "context" in Great Expectations. The context is the primary access point to all configurations and functions that we'll use for validating our data.

To initialize the Great Expectations context, you'll use a method from the Great Expectations library. The context will be your primary interface for most operations.

```python
context = gx.get_context()
```

📚 [Great Expectaions documentation](https://docs.greatexpectations.io/docs/terms/data_context/)

<br>

# 2️⃣ Setup our expectations:

Open `data-source.ipynb` and define the expectations!

In this step we will create a `validator` and save it for later use in our scraper pipeline! Make sure you complete the validations for each column!

<br>

# 3️⃣ Use the expectation suite:

You are now ready to use the expectations suite and need to code `run_expectations` inside `expecations.py`. The package is quite finicky at this stage so if you get stuck don't be afraid to use the hints. Once you have the code reusing it for your own use cases is much easier!

### 3.1. Begin by initializing the Great Expectations context.

This context provides access to all the configurations and functions of Great Expectations.

<details>
<summary markdown='span'>Hint</summary>

To initialize the context:

```python
context = gx.get_context()
```

</details>

### 3.2. Configuring the Datasource:

Datasources in Great Expectations represent the origins of your data. For this task, you'll be setting up a pandas datasource.

<details>
<summary markdown='span'>Hint</summary>

To configure a pandas datasource:

```python
datasource = context.sources.add_or_update_pandas(name="hn_df")
```

</details>

### 3.3. Setting up the Data Asset:

A data asset is a specific entity within your datasource. Here, you'll link your DataFrame to a data asset.

<details>
<summary markdown='span'>Hint</summary>

To define a data asset:

```python
data_asset = datasource.add_dataframe_asset(name="hn_df")
```

</details>

### 3.4. Building the Batch Request:

A batch in Great Expectations refers to a specific portion of a data asset, which you want to validate against your expectations.

<details>
<summary markdown='span'>Hint</summary>

To construct a batch request:

```python
batch_request = data_asset.build_batch_request(dataframe=df)
```

</details>

### 3.5. Creating a Checkpoint:

Checkpoints are a way to bundle together one or more batches with one or more Expectation Suites, and then validate them.

<details>
<summary markdown='span'>Hint</summary>

To set up a checkpoint:

```python
checkpoint = context.add_or_update_checkpoint(
    name="check_hn",
    validations=[
        {
            "batch_request": batch_request,
            "expectation_suite_name": "hn_expectation_suite",
        }
    ],
)
```

</details>

### 3.6. Running the Checkpoint:

Now, execute the checkpoint to validate the data against the expectations.

<details>
<summary markdown='span'>Hint</summary>

To run the checkpoint:

```python
checkpoint_result = checkpoint.run()
```

</details>

### 3.7. Generating Documentation:

Build data documentation to have a visual representation of your data validation results.

<details>
<summary markdown='span'>Hint</summary>

To produce data documentation:

```python
context.build_data_docs()
```

</details>

### 3.8. Analyzing the Validation Results:

After validation, inspect the results to check if the data matches the expectations. If there are discrepancies, use the `send_message` function to notify about the failed expectations.

<details>
<summary markdown='span'>Hint</summary>

You can loop through the validation results and identify any failed expectations. Depending on the results, you can send notifications about the success or failures:

```python
failures = []
for expectation_result in ...:  # Iterate over validation results
    if not expectation_result["success"]:
        failures.append(expectation_result)

if failures:
    for failure in failures:
        send_message("Expectation failed!")
        # More details about the failure can be sent using send_message
else:
    send_message("All expectations passed!")
```

</details>

<br>

# 4️⃣ Testing 🧪:

Run your code with:

```bash
python scraper/main.py
```

And checkout the results in the channel and the data docs!

🧪 Once you are satisfied it works - run the tests:

```bash
make test
```
<br>

# 🏁 Finish

We are now using great expectation to maintain the quality of our data. This is a slow process but is essential to preventing your data lake from becoming a data swamp!

Don't forget to push your code to github so Kitt can track your progress!

<br>
