# 🎯 Goals

The goal of this recap is to show how to deploy a DBT pipeline from a development environment to a production environment.

❗ If students haven't completed the **Materialization** section of **DBT Test and Materialization** challenge, it could be worth briefly covering.

<br>

# 1️⃣ Development and Production

At the moment we have been developing and creating models in a **development environment**. How would we push our tables to a **production environment**?

In a professional environment, you would not create models and push those models to production tables in your data warehouse while developing them. A more likely scenario is that you would be working on a (representative) sample of the data to develop your models, when you are happy with how they are working, apply your pipeline to your full, raw production data.

Remembering that the warehouses engine itself is powering the transformations defined in your models. Working on a sample of your data would be more cost efficient, and the models would also take less time to run.

DBT has a way to manage development and production (and many more) environments with a mechanism called **targets**.

Your target is defined in your `profiles.yml` located at `~/.dbt/profiles.yml`. Open it in VS Code and take a look:

```bash
code ~/.dbt/profiles.yml
```

It should look similar to the below:

```yaml
# ~/.dbt/profiles.yml

dbt_lewagon:
  outputs:
    dev: # target name
      dataset: dbt_<your_name>_day1 # e.g: dbt_tswift_day1
      job_execution_timeout_seconds: 300
      job_retries: 1
      keyfile: /home/<user_name>/.gcp_keys/wagon-de-vm-sa.json
      location: EU
      method: service-account
      priority: interactive
      project: <your_GCP_project_id>
      threads: 1
      type: bigquery
  target: dev # your default target
```

The default target for whenever you run: `dbt run`, `dbt test`, or `dbt build` is the output value defined in the `target` key. It should currently be `dev`. To create a new target, for example `prod`, create a new key with the targets' name inside of the `outputs` key, then duplicate the contents of `dev` with a different dataset.

❓ Create a `prod` target with the target dataset of `dbt_<your_name>_day1_prod`. If your name was Taylor Swift, the dataset would be called: `dbt_tswift_day1_prod`.

<details>
<summary markdown='span'>🎁 Solution</summary>

```yaml
# ~/.dbt/profiles.yml

dbt_lewagon:
  outputs:
    dev: # target name
      dataset: dbt_<your_name>_day1 # e.g: dbt_tswift_day1
      job_execution_timeout_seconds: 300
      job_retries: 1
      keyfile: /home/<user_name>/.gcp_keys/wagon-de-vm-sa.json
      location: EU
      method: service-account
      priority: interactive
      project: <your_GCP_project_id>
      threads: 1
      type: bigquery
    prod: # target name
      dataset: dbt_<your_name>_day1_prod # e.g: dbt_tswift_day1_prod
      job_execution_timeout_seconds: 300
      job_retries: 1
      keyfile: /home/<user_name>/.gcp_keys/wagon-de-vm-sa.json
      location: EU
      method: service-account
      priority: interactive
      project: <your_GCP_project_id>
      threads: 1
      type: bigquery
  target: dev # your default target
```

</details>

When you have finalised your `profiles.yml`, **build** your pipeline with the correct target:

```bash
dbt build --target prod
```

And check BigQuery to check the materialization of your tables. It should look similar to the below:

<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/030204-dbt-bigquery-prod-materialization.png">


At the moment we are materializing the **prod** target into the same GCP Project as your **dev** target. But by changing some parameters in your `profiles.yml`, you can see how you could apply your pipeline to two different GCP Projects, one with your development data, and one with your production data.

<br>

# 2️⃣ Dynamic Sources

There is much more you can do with DBT in terms of targets, for example dynamically changing the **source** data based on the **target**.

❗ Requires creating a new dataset called `raw_gz_data_devsample` and three new tables:
- **raw_gz_product**
- **raw_gz_sales**
- **raw_gz_ship**

<details>
<summary markdown='span'>🎁 Create BigQuery devsample assets</summary>

Download sampled data:

```bash
mkdir -p data/2021_07-devsample

curl -o ./data/2021_07-devsample/raw_gz_sales-2021_07_devsample.parquet https://wagon-public-datasets.s3.amazonaws.com/data-engineering/raw_gz_sales-2021_07_sample.parquet
curl -o ./data/2021_07-devsample/raw_gz_product-2021_07_devsample.parquet https://wagon-public-datasets.s3.amazonaws.com/data-engineering/gz_raw_data-raw_gz_product.parquet
curl -o ./data/2021_07-devsample/raw_gz_ship-2021_07_devsample.parquet https://wagon-public-datasets.s3.amazonaws.com/data-engineering/raw_gz_ship-2021_07_sample.parquet
```

❗ Note the product table hasn't been sampled. It is a relatively small table. For this example it's not worth the effort to go through and sample down to the products sold in the target dev period.

Create BigQuery dataset:

```bash
# don't forget to put in your project id
bq mk --location=EU --dataset <your_gcp_project_id>:raw_gz_data_devsample
```

Upload data to BigQuery:

```bash
bq load --autodetect \
    --source_format=PARQUET \
    --location=EU \
    raw_gz_data_devsample.raw_gz_sales \
    ./data/2021_07-devsample/raw_gz_sales-2021_07_devsample.parquet

bq load --autodetect \
    --source_format=PARQUET \
    --location=EU \
    raw_gz_data_devsample.raw_gz_product \
    ./data/2021_07-devsample/raw_gz_product-2021_07_devsample.parquet

bq load --autodetect \
    --source_format=PARQUET \
    --location=EU \
    raw_gz_data_devsample.raw_gz_ship \
    ./data/2021_07-devsample/raw_gz_ship-2021_07_devsample.parquet
```

</details>

Imagine a scenario where you have two GCP Projects:
- **finance_project** - where the finance team source there data.
    - where the **source** dataset was named: `raw_gz_data`
    - `raw_gz_sales` with 1,375,630 records between 2021-04-01 and 2021-09-30.
    - `raw_gz_ship` with 167,552 records for the above fact table
- **data_eng_project** - your development playground where you can cause errors with no (or less) consequences.
    - where the **source** dataset was named: `raw_gz_data_devsample`
    - Sampled `raw_gz_sales` with 205,642 records with one month of data between 2021-07-01 and 2021-07-31
    - Sampled `raw_gz_ship` with 25,703 records for the above sampled fact table

DBT will try to source data based on targets. Because the **source** dataset has a different name, you need a way to reference the correct BigQuery dataset based on your target. This would be a non-issue if the name of the dataset in both projects had the same name, but the same idea applies to table names, projects, etc.

Like Python and Airflow, DBT creates variables at runtime. We can access runtime variables with Jinja templating and execute conditional statements with Jinja templating in `.yml` files. A odd feature because `.yml` files were specifically designed to be static.

Explicit syntax for two or more targets:

```yaml
# models/source/sources.yml

version: 2

sources:
  - name: raw
    schema: |
      {%- if target.name == "dev" -%} raw_gz_data_devsample
      {%- elif target.name == "prod" -%} raw_gz_data
      {%- else -%} invalid_target
      {%- endif -%}
    tables:
      - name: sales
        identifier: raw_gz_sales
        description: sales of Greenweez. One row per product_id found in each orders_id
        ...snip...
```

More pythonic syntax for two targets:

```yaml
# models/source/sources.yml

version: 2

sources:
  - name: raw
    schema: "{{ 'raw_gz_data_devsample' if target.name == 'dev' else 'raw_gz_data' }}"
    tables:
      - name: sales
        identifier: raw_gz_sales
        description: sales of Greenweez. One row per product_id found in each orders_id
        ...snip...
```

Once the change has been made, execute a run against both targets:

```bash
# dev
dbt run --target dev

# prod
dbt run --target prod
```

And pay close attention to the number of rows created for the mart layer table: `finance_days` for both runs. The **dev** run should have created a table with less rows! Now you have two different targets AND are developing on a sample of the data.

❗ We created tables in our **raw_gz_data_devsample** dataset with the exact same name as our **raw_gz_data** dataset. You can change table names, but it will make your `sources.yml` more verbose if you use this method.

You can apply this kind of idea to different parts of your DBT project. For example, maybe you want to materialize all of the staging and intermediate layers for both dev and prod targets to a single project, then materialize the **mart** layer of the **prod** target into a different GCP Project.

<br>

# 🏁 Finishing up

There are a number of different ways you can apply Jinja templating to your DBT project. We have only just scratched the surface. DBT has fantastic documentation for further reading.

To take DBT further, here are some suggestions:
- Project **variables** in DBT at [this link](https://docs.getdbt.com/docs/build/project-variables)
- Using **environment variables** in DBT at [this link](https://docs.getdbt.com/docs/build/environment-variables). Another useful way of differentiating between development and production environments.
- Using Jinja to **centralise your documentation** at [this link](https://docs.getdbt.com/reference/dbt-jinja-functions/doc). Especially useful when you have the same column description over multiple models.
- Explore other external packages like **dbt_expectations** at [this link](https://hub.getdbt.com/calogica/dbt_expectations/latest/) is a package inspired by the python package Great Expectations for data quality and assurance.

If you want more practice in creating models and config files, you'll find a set of archived challenges in the `legacy/` folder.

<br>
