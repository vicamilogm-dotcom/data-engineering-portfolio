# Streaming with queues!

When there is too much data to handle for our workers, when data flow needs to be managed, or processing scheduled, **queues** come to the rescue.

**Pub/Sub** at its core is a messaging service. It can be leveraged in multiple use-cases where real-time or event driven data transfer is required. **Pub/Sub** is fully managed by GCP and can be easily integrated with other GCP or open-source services.

🎯 In this Challenge, we will create a **Pub/Sub Topic** and publish real-time data. Then, we will stream this data via a **subscriber** to transform the data and load it to **BigQuery**.



# 1️⃣ Topic Creation 📕

we would create a new Pub/Sub Topic. From the Navigation Menu select Pub/Sub

In the Pub/Sub page (Enable Pub/Sub API if prompted to), click on create topic

You can name it `data-stream` as the below example:

<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W3D4/0403-03-topic_creation.png" witdh=200>

<details>
<summary markdown='span'>💡 Create topic in the cli</summary>

```bash
gcloud pubsub topics create <topic name>
```

</details>


Store your topic id in your .env within the variable `TOPIC_NAME` and make sure to reload your direnv.
You can test that it has been stored by executing this command:
```bash
echo $TOPIC_NAME
```

❗If it is not working even after a `direnv reload`, make sure to have a `dotenv` line in your .envrc file


By default a subscription is created as `\<Topic id\>-sub`. **Let's publish** the first message in the console and pull it via the gcp console subscriber

We can see the Pub/Sub in action by clicking on your topic Id and clicking on Publish Message via the tab Messages 👇

<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W3D4/0403-03-create_message.png" width=700>

❓ For now write “Hello World” in the message box **and click on Publish**
<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W3D4/0403-03-publish_message.png" width=700>

Once the message is published, we can go back to our subscription page to pull and receive the message. **Follow the instructions  in the image below** 👇

<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W3D4/0403-03-pull_message2.png" width=700>


❗️ Once the message is **acknowledged** (**ack**), it is flushed from the **queue** and won't be sent anymore.

Now that we Have seen how to subscribe to a message in the UI, let's code it in python 🐍.
It'll help receive high quantities of messages and apply transformations to them as they come in!

# 2️⃣ Creating a subscriber 🤓

❓ **Fill in the .env** with the variables: **PROJECT_ID** and **SUBSCRIPTION_NAME**

❓ Now head to the file `subscriber-basics.py` and implement the run function by following the comments inside the function.

👉 Now Let's code the callback function. This callback function is meant to be called at each published message
during the subscription. For a simple subscriber, let's just print the message and ack it.
<br>

❗️ Don't forget to **ack** every message, otherwise it will be kept sent by pubsub.

Launch the subscriber with this command

```python
python app/subscriber-basics.py
```

Notice that the **subscriber** is now waiting for new messages.
Create some on gcp console as we have done on the first part of the challenge. You should see them coming in the terminal like below 👇

<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W3D4/terminal-sub-basic.png">

Now we can implement a **publisher** to send the **real-time** data from challenge one.

# 3️⃣ Publish data ✍️

Back to the first challenge of the day: real-time streaming 💪. To stream the data we first need to source it. Let’s simulate multiple sensors publishing to the same **topic** in **pub/sub**.

Head to `app/publisher.py`. You’ll notice that there is already a get message that generates a message for a specific sensor as we have seen in the first Challenge

👉 following the comments inside the function `run`.

Now you can publish a message once it is generated!

❗️ The **message** must be a **byteString** to be published in Pub/Sub

Let's open a new terminal and launch the publisher and let it publish some messages before to stop it with `ctrl+c`
Launch the publisher with this command

```python
python app/publisher.py
```

Now Launch the subscriber with this command

```python
python app/subscriber-basics.py
```

Even if the publisher is stopped, the subscriber unstacked the queue and ack messages. The messages stays in the pubsub queue until they are acked

you can lauch simultanously in two diffferent terminal the subscriber and the publisher<br>
💪 We are streaming data in real-time!

Now lets subscribe to the data with Apache Beam and make some transformations before loading the data into BigQuery

# 4️⃣ Subscriber with Apache beam

First Let's head to subscriber `app/subscriber-beam.py` and go to the `run` function!

The structure of the pipeline:

- data: Pull data from Pub/Sub Topic
- windowing: Round off the timestamp to an range interval
- grouping: aggregate the records per sensor per interval
- out: Write the data to BigQuery

We have already implemented the main structure with the file example earlier, now we have to adapt it to streaming mode.

❓ For the data part of the pipeline, where do you think we can source the data from ?

<details>
<summary markdown='span'>💡 Answer</summary>

Directly from pubsub with apache beam!

</details>

## 4.1 Data

❓ Implement the data section to read the data from pub/sub and decode it!

To check that works run the following command:
```python
python app/subscriber-beam.py --id $PROJECT_ID --subscription-name $SUBSCRIPTION_NAME
```
In another terminal **now start the publisher**. It should look something like this 👇

<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W3D4/data-streaming-1.png">

For now your are streaming the data and printing it to the terminal. Thanks to

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


## 4.2 Windowing and grouping!

For that we need a windowing and grouping pipeline.

In the previous challenge, we already implemented those two parts.

❓ Add the code from the previous exercise into the **window** and **group sections** now, let's keep the same implementation and try to execute the pipeline with the following command:

```python
python app/subscriber-beam.py --id $PROJECT_ID --subscription-name $SUBSCRIPTION_NAME
```

😅 You should get the following error:

```bash
ValueError: GroupByKey cannot be applied to an unbounded PCollection with global windowing and a default trigger
```

Before, we had access to **all the data** before executing the transformation.

🤔 During the streaming what could be problematic for grouping?

<details>
  <summary markdown='span'>💡 Explanations</summary>

With an unbounded data set, it is impossible to collect all of the elements, since new elements are constantly being added and may be infinitely many.<br>
Beam’s default windowing behavior is to assign all elements of a PCollection to a single, global window.
Before you use a grouping transform such as GroupByKey on an unbounded PCollection, you must at least set a non-global windowing function such as Fixed-time windows to gather data within a time window and trigger the grouping.

</details>


❓ **Implement a windowing pipeline**. You can have a look to this example in the [programming guide](https://beam.apache.org/documentation/programming-guide/#using-fixed-time-windows). Also refer to the **example** from the lecture.

Our workflow is:
- Attach a timestamp
- Put our element into key, value format: (timestamp_rounded, [iot data])
- Finally create fixed windows of our interval size!

We are now ready to test if this works. But first let's **make sure to empty the queue.**

❓ Run your updated **subscriber** along with the publisher

In the terminal which is running the subscriber, make sure that every 15 seconds approximately a new line is printed with the grouped data per sensor in a dictionary. Like below 👇

<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W3D4/data-streaming-2.png" width=700>

Now We are ready to load the data to BigQuery!

## 4.3 Load to BigQuery

❓ First let's create a new table `stream` in your big query dataset with the right schema:

Under schema click on Edit as text and paste the following schema:

```bash
Timestamp:TIMESTAMP, Airtight:FLOAT, AtmP:FLOAT, H2OC:FLOAT, Temp:FLOAT
```

**📝 Now fill in the `BQ_TABLE` variable in your `.env`**
with the right format:
```bash
BQ_TABLE=<your-project-id>:<your-bq-dataset-name>.<your-table-name>
```

👉 Let's head to the `out_bq` part of the pipeline and add `Write to Big Query` transformation using
[beam.io.gcp.WriteToBigQuery](https://beam.apache.org/releases/pydoc/2.8.0/apache_beam.io.gcp.bigquery.html)


Since we are streaming data, choose the corresponding `write_disposition` parameter for our task.

Let's make sure that it works by running the following command along with a publisher!:
```python
python app/subscriber-beam.py \
--id $PROJECT_ID \
--subscription-name $SUBSCRIPTION_NAME \
--output-table $BQ_TABLE
```

Let's head to your gcp console into BigQuery and check that the live streaming is working well

# 🏁Conclusion
Congratulation🎉 Tou have build a complete real-time Data Streaming ETL pipeline.

Don't for get to commit and push your code to github!


# (Bonus) Deploy the pipeline to Dataflow

The Google Cloud Dataflow Runner uses the Cloud Dataflow managed service. When you run your pipeline with the Cloud Dataflow service, the runner uploads your executable code and dependencies to a Google Cloud Storage bucket and creates a Cloud Dataflow job, which executes your pipeline on managed resources in Google Cloud Platform.

Deployment into Dataflow is easy with Apache Beam, we just have to change the runner option of the pipeline and give the right GCP parameters.
Here is the [documentation](https://beam.apache.org/documentation/runners/dataflow/) of the needed parameters

To add a parameters to the pipeline you can use command-line arguments when you execute the subscriber-beam.py script as follow:

```bash
--runner DataflowRunner
```

You can fill in your `.env` the following variable to be used in your command line :
- PROJET_ID
- BUCKET_NAME
- REGION

<details>
  <summary markdown='span'>💡 Hints</summary>

```bash
python app/subscriber-beam.py \
    --id $PROJECT_ID \
    --subscription-name $SUBSCRIPTION_NAME \
    --output-table $BQ_TABLE \
    --runner DataflowRunner \
    --project $PROJECT_ID \
    --streaming true \
    --temp_location gs://$BUCKET_NAME/temp \
    --staging_location gs://$BUCKET_NAME/staging \
    --region europe-west4
```

</details>

Now you can head to Dataflow service within GCP, have a look to your dataflow graph by clicking on the active job name.

Once it is ready you can launch your publisher:

```python
python app/publisher.py
```


# (Bonus) TimeWindow Session for robustness 😅

🎯 modify pipeline windowing

- Create `beam.window.TimestampedValue`
- Apply `beam.WindowInto`
- Apply a `MapSessionWindow` by getting the window end time within the function process of the class

Why do we need a trigger?
In real time there is no way to group data because we don't have it yet. We have then to trigger the grouping repeatedly.
