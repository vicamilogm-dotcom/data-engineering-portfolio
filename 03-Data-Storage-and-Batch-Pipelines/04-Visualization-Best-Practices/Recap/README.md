# Recap

The recap of the day should involve the students presenting and explaining what they have made!

<br>

# End to End Architecture

## Formula 1 sample architecture

If there is additional time at the end of the session, talk about the archicture of a pipeline that uses Airbyte, Airflow, BigQuery, and Streamlit for an end to end example.

Our current architecture is using streamlit and postgres in a docker compose stack, using a static dataset.

We can use our Airflow knowledge to orchestrate the process from a production database or data lake.

You could separate the stack and automate the workflow by using Airflow so the dashboard was up to date on an arbitrary schedule. An example architecture could be:
- Assuming your production data is (replicated) in a postgres instance, located on a separate server or fully managed.
- Deploy Streamlit in a stand alone container on GCP Cloud Run or [Streamlit Cloud](https://streamlit.io/cloud)
- Have the Streamlit app connect to either a warehouse like BigQuery, better for analytical queries, with a dedicated GCP Service Account and Key.
- Use Airflow and create a DAG to move the data between your postgres instance/data lake to BigQuery and create views that your Streamlit app will query from. There is a number of ways you can use Airflow to move your data:
    - Between your production db/data lake and BigQuery:
        - You can temporarily download the data to the the Airflow host (be wary of memory)
        - Build an API with FastAPI and use python to ingest, perform the transform and dump to BigQuery.
        - Use Airbyte on a separate node.
    - Between BigQuery layers:
        - Just use Airflow BigQuery operators if the transforms are simple.
        - Use dbt for more complex data models
- Now your Dashboard will always have up to date data on whatever schedule you choose!

See below for a sample architecture diagram for the F1 Dashboard:

![](https://wagon-public-datasets.s3.amazonaws.com/data-engineering/03040R-f1-pipeline-architecture.png)

<br>

## Generic Bronze, Silver, Gold Architecture

This is a larger, more generic architecture diagram that you could use to implement a pipeline with Bronze, Silve, Layers using tools that we've already covered.

![](https://wagon-public-datasets.s3.amazonaws.com/data-engineering/0304-generic-bronze-silver-gold-architecture-diagram.png)

❗ Remember, this isn't the only way to create and orchestrate a pipeline. There are many alternate technologies and tools that you could use to achieve the same outcome!

As a class, talk through this architecture diagram and understand how data is flowing. Some ideas to expand on are:
- How does this diagram differ from the previous one.
- Can you think of any more sources to ingest from, what tools or frameworks would you use to facilitate the data ingestion?
- How could you expand the _Serve_ section to service ML workloads or other end users in a business?
- What is the ideal file format for a data lake?
    <details>
    <summary markdown='span'>🎁 Answer</summary>

    Almost always `.parquet`!

    Why? [Compression](https://en.wikipedia.org/wiki/Run-length_encoding). If the source data is smaller, the cost of storage is cheaper, but also the ingress and egress cost will be significantly lower.
    </details>

<br>
