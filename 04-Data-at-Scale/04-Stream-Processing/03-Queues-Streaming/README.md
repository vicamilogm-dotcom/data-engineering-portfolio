# 🎯 Streaming with queues!

When there is too much data to handle for our workers, when data flow needs to be managed, or processing scheduled, **queues** come to the rescue.

**Pub/Sub** at its core is a messaging service. It can be leveraged in multiple use-cases where real-time or event driven data transfer is required. **Pub/Sub** is fully managed by GCP and can be easily integrated with other GCP or open-source services.

🎯 In this Challenge, we will create a **Pub/Sub Topic** and publish real-time data. Then, we will stream this data via a **subscriber** to transform the data and load it to **BigQuery**.

<br>

# 1️⃣ Topic Creation 📕

We will create a new Pub/Sub Topic. From the Navigation Menu select Pub/Sub.

In the Pub/Sub page (Enable Pub/Sub API if prompted to), click on create topic.

You can name it `data-stream` as in the below example:

<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W3D4/0403-03-topic_creation.png" witdh=200>

<details>
<summary markdown='span'>💡 Create a topic in the cli</summary>

```bash
gcloud pubsub topics create <topic name>
```

</details>


Store your Topic ID in your .env in the variable `TOPIC_NAME` and make sure to reload your direnv.
You can test that it has been stored by executing this command:
```bash
echo $TOPIC_NAME
```

❗If it is not working even after a `direnv reload`, make sure to have a `dotenv` line in your .envrc file.


By default a subscription is created as `\<Topic id\>-sub`. **Let's publish** the first message in the console and pull it via the GCP console subscriber.

We can see the Pub/Sub in action by clicking on your topic Id and clicking on Publish Message via the tab Messages 👇

<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W3D4/0403-03-create_message.png" width=700>

❓ For now write “Hello World” in the message box **and click on Publish**
<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W3D4/0403-03-publish_message.png" width=700>

Once the message is published, we can go back to our subscription page to pull and receive the message. **Follow the instructions  in the image below** 👇

❗ If you created the Pub/Sub topic with the CLI, you might not have a default subscriber. Create one from the Subscribions tab.

<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W3D4/0403-03-pull_message2.png" width=700>


❗️ Once the message is **acknowledged** (**ack**), it is flushed from the **queue** and won't be sent anymore.

Now that we have seen how to subscribe to a message in the UI, let's code it in python 🐍.
It will help receive high quantities of messages and apply transformations to them as they come in!

<br>

# 2️⃣ Creating a subscriber 🤓

❓ **Fill in the .env** with the variables: **PROJECT_ID** and **SUBSCRIPTION_NAME**

❓ Now head to the file `subscriber_basics.py` and implement the **run** function by following the comments inside the function.

❓ Now let's code the **callback** function. This callback function is meant to be called at each published message during the subscription. For our simple subscriber, let's just print the message and _ack_ it.

❗️ Don't forget to **ack** every message, otherwise Pub/Sub will continue sending it.

Launch the subscriber with:

```bash
python app/subscriber_basics.py
```

Notice that the **subscriber** is now waiting for new messages.

Create some messages in the GCP console like we did in the first part of the challenge. You should see them appearing in the terminal like below 👇

<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W3D4/terminal-sub-basic.png">

Now we can implement a **publisher** to send the **real-time** data from the previous challenge.

# 3️⃣ Publish data ✍️

Back to the first challenge of the day: real-time streaming 💪. To stream the data we first need to source it. Let’s simulate multiple sensors publishing to the same **topic** in **Pub/Sub**.

Head to `app/publisher.py`. You’ll notice that there is already a `get_message_data` method that generates a message for a specific sensor like in the first challenge.

👉 Follow the comments inside the function `run`.

Now you can publish a message once it is generated!

❗️ The **message** must be a **byteString** to be published in Pub/Sub

Let's open a new terminal and launch the publisher and let it publish some messages before we stop it with `ctrl+c`.

Launch the publisher with this command:

```python
python app/publisher.py
```

Now launch the subscriber with this command:

```python
python app/subscriber_basics.py
```

Even if the publisher is stopped, the subscriber unstacked the queue and acked the messages. The messages stays in the Pub/Sub queue until they are acked.

You can lauch the publisher and the subscriber simultanously in two different terminals.<br>
💪 We are streaming data in real-time!

Now let's subscribe to the data with Apache Beam and make some transformations before loading the data into BigQuery.

<br>

# 4️⃣ Subscriber with Apache beam

First head to subscriber `app/subscriber_beam.py` and go to the `run` function!

The structure of the pipeline:

- data: pull data from the Pub/Sub Topic
- windowing: round off the timestamp to make intervals
- grouping: aggregate the records per sensor per interval
- out: write the data to BigQuery

We have already implemented the main structure with the file example earlier, now we have to adapt it to streaming mode.

❓ For the data part of the pipeline, where do you think we can source the data from ?

<details>
<summary markdown='span'>💡 Answer</summary>

Directly from Pub/Sub with Apache Beam!

</details>

## 4.1. Data

❓ Implement the data section to read the data from Pub/Sub and decode it!

To check that it works run the following command:
```python
python app/subscriber_beam.py --id $PROJECT_ID --subscription-name $SUBSCRIPTION_NAME
```
In another terminal **start the publisher**. It should look something like this 👇

<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W3D4/data-streaming-1.png">

For now you are streaming the data and printing it to the terminal thanks to this line:

```python
group | "Print debug" >> beam.Map(lambda x: print(x))
```

At the end of the pipeline you can use this throughout to help you debug!

Let's first shutdown the **publisher** and then the **beam subscriber**, so that we make sure that no data remains in the queue.

<details>
<summary markdown='span'>🕵️ Ack all messages in your queue</summary>

```bash
gcloud pubsub subscriptions seek $SUBSCRIPTION_NAME --time "2025-01-01T00:00:00Z"
```

</details>


## 4.2. Windowing and grouping!

For that we need a windowing and grouping pipeline.

In the previous challenge, we already implemented those two parts.

❓ Add the code from the previous exercise into the **window** and **group sections**. Let's keep the same implementation and try to execute the pipeline with the following command:

```python
python app/subscriber_beam.py --id $PROJECT_ID --subscription-name $SUBSCRIPTION_NAME
```

😅 You should get the following error:

```bash
ValueError: GroupByKey cannot be applied to an unbounded PCollection with global windowing and a default trigger
```

Before, we had access to **all the data** before executing the transformation.

🤔 During the streaming what could be problematic for grouping?

<details>
  <summary markdown='span'>💡 Explanations</summary>

With an unbounded data set, it is impossible to collect all of the elements, since new elements are constantly being added and it may be an infinite stream.

Beam’s default windowing behavior is to assign all elements of a PCollection to a single, global window.
Before you use a grouping transform such as `GroupByKey` on an unbounded PCollection, you must at least set a non-global windowing function such as Fixed-time windows to gather data within a time window and trigger the grouping.

</details>

❓ **Implement a windowing pipeline**. You can have a look at this example in the [programming guide](https://beam.apache.org/documentation/programming-guide/#using-fixed-time-windows). Also refer to the **example** from the lecture.

Our workflow is:
- Attach a timestamp
- Put our element into key, value format: (timestamp_rounded, [iot data])
- Finally create fixed windows of our interval size!

We are now ready to test if this works. But first let's **make sure to empty the queue.**

❓ Run your updated **subscriber** along with the publisher

In the terminal which is running the subscriber, make sure that every 15 seconds approximately a new line is printed with the grouped data per sensor in a dictionary. Like below 👇

<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W3D4/data-streaming-2.png" width=700>

Now We are ready to load the data to BigQuery!

## 4.3. Load to BigQuery

❓ First let's create a new table `iot_beam_stream` in your BigQuery dataset with the right schema:

Under schema click on Edit as text and paste the following schema:

```bash
Timestamp:TIMESTAMP, Airtight:FLOAT, AtmP:FLOAT, H2OC:FLOAT, Temp:FLOAT
```

**📝 Now fill in the `BQ_TABLE` variable in your `.env`**
with the right format:

```bash
BQ_TABLE=<your-project-id>.<your-bq-dataset-name>.<your-table-name>
```

👉 Let's head to the `out_bq` part of the pipeline and add `Write to Big Query` transformation using
[beam.io.gcp.WriteToBigQuery](https://beam.apache.org/releases/pydoc/2.8.0/apache_beam.io.gcp.bigquery.html)

Since we are streaming data, choose the corresponding `write_disposition` parameter for our task. We also do not need to include a temp staging area with the correct `write_disposition`. 😉

Let's make sure that it works by running the following command along with a publisher!:
```bash
python app/subscriber_beam.py \
--id $PROJECT_ID \
--subscription-name $SUBSCRIPTION_NAME \
--output-table $BQ_TABLE
```

Let's head to your GCP console into BigQuery and check that the live streaming is working well

<br>


# 5️⃣ (Optional) Deploy the pipeline to Dataflow

The Google Cloud Dataflow Runner uses the Cloud Dataflow managed service. When you run your beam pipeline with the Cloud Dataflow service, the runner uploads your executable code and dependencies to a Google Cloud Storage bucket and creates a Cloud Dataflow job, which executes your pipeline on managed resources in Google Cloud Platform.

Deployment into Dataflow is relatively easy with Apache Beam, we just need a few extra things:
1. Build our poetry package into a `.whl` - required because our beam pipeline is more than one python script.
1. We need to change the runner option of the pipeline and provide some additional GCP parameters. Here is the [documentation](https://beam.apache.org/documentation/runners/dataflow/) of the required parameters.

## 5.1. Build a wheel 🛞

❗ By default, the GCP Dataflow runner will only upload the target file to be executed. Because we have used a helper function, `aggregate_sensors`, in a separate file, `app/utils.py`, we need a way to upload all of our code and dependencies. We are using **poetry** as our package manager, and poetry provides an easy way to **build** our package into a standardized binary package format called `.whl`.

By including the our package `.whl`, the Dataflow runner has everything it needs to execute our pipeline!

Create a `.whl` of your python package:

```bash
poetry build
```

The output should look similar to:

```txt
Building beam-stream (0.1.0)
  - Building sdist
  - Built beam_stream-0.1.0.tar.gz
  - Building wheel
  - Built beam_stream-0.1.0-py3-none-any.whl
```

This will have created a new directory in your project root named: `dist/` with two files inside:
- `beam_stream-0.1.0.tar.gz` - essentially a zipped archive of your package
- `beam_stream-0.1.0-py3-none-any.whl` - pre-compiled binaries of your package

If you can't see the `dist/` directory in your VS Code explorer, don't worry. VS Code may be hiding some directories in the file explorer - directories like `.git` and `dist`. In your integrated terminal, run:

```bash
ls
```

From your project root to confirm the `dist/` directory is there.

When using a `.whl` file as part of your Dataflow deployment, the additional required flag is:

```bash
--extra_package dist/<your_python_package.whl>
```

Alternatively, you could move the `aggregate_sensors` function into `app/subscriber_beam.py` and bypass building a wheel for your package. For completeness and continuity we have include it.

## 5.2. Additional parameters

To add extra parameters to the pipeline you can use command-line arguments when you execute the `subscriber_beam.py` script as follows:

```bash
--runner DataflowRunner
```

These arguments will be passed on to our `beam.Pipeline` through the `pipeline_args`.

You can fill in your `.env` the following variable to be used in your command line :
- `PROJET_ID`
- `BUCKET_NAME`

<details>
  <summary markdown='span'>💡 Hint</summary>

```bash
python app/subscriber_beam.py \
    --id $PROJECT_ID \
    --subscription-name $SUBSCRIPTION_NAME \
    --output-table $BQ_TABLE \
    --runner DataflowRunner \
    --project $PROJECT_ID \
    --streaming \
    --temp_location gs://$BUCKET_NAME/temp \
    --staging_location gs://$BUCKET_NAME/staging \
    --extra_package dist/beam_stream-0.1.0-py3-none-any.whl \
    --region europe-west4
```

If you try to deploy your beam pipeline to GCP Dataflow and get an error, you may need to enable the Dataflow API on your GCP project. Read the error carefully and see if there is a link to enable the Dataflow API.

</details>

## 5.3. See the results!

Now you can head to Dataflow service within GCP, have a look at your dataflow graph by clicking on the active job name. To see more detail, expand the **Logs** section at the bottom of the page. There are logs for the overall job, and logs for each individual worker note.

Once it is ready you can launch your publisher:

```bash
python app/publisher.py
```

Have a look at your Dataflow job and you should see the number of elements per second being processed.

After a while, refresh BigQuery and you should see new records in your table! 🎉

## 5.4. Teardown 🔨

To avoid any unwanted costs, make sure you teardown your pipeline once you've completed the challenge! By default a beam pipeline is deployed on a n1-standard-2 Compute Engine instance.

Make sure to first stop your `publisher.py` script.

To teardown your pipeline:

```bash
# List all dataflow jobs - region in the form: europe-west4
gcloud dataflow jobs list --region <region>

# Drain or cancel the target job
gcloud dataflow jobs drain <job_id> --region <region>
gcloud dataflow jobs cancel <job_id> --region <region>

# Confirm the job has been cancelled - the state should be updated
gcloud dataflow jobs list --region <region>
```

Alternatively you can stop a Dataflow job through the GCP Console:
- Starting from the [Dataflow jobs page](https://console.cloud.google.com/dataflow/jobs)
- Click on the Dataflow job you want to stop
- Click **stop** at the top of the page
- Select drain or cancel in the pop up menu, then click on **Stop job**:
    - **Drain** allows the pipeline to gracefully stop by processing any data that is already in flight. It ensures that no new work is accepted, but any work already started will complete before the instance is terminated.
    - **Cancel** will cancel the job and terminate the instance. Any in flight data is lost.

<br>

# 🏁 Finishing up

Congratulations! 🎉 You have build a complete real-time Data Streaming ETL pipeline.

Don't forget to git add, commit, and push your code to GitHub so you can track your progress on Kitt!

<br>

# (Bonus) TimeWindow Session for robustness 😅

🎯 Modify pipeline windowing:

- Create `beam.window.TimestampedValue`
- Apply `beam.WindowInto`
- Apply a `MapSessionWindow` by getting the window end time within the function process of the class

❓ Why do we need a trigger?

In real time there is no way to group data because we don't have it yet. We have to trigger the grouping repeatedly.

<br>
