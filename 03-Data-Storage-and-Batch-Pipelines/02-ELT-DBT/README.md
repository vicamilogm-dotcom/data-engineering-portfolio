## Prerequisites

Make sure you've
- Enabled the BigQuery API and can run `gcloud` commands in your terminal

## Recap from last module and high level view of the unit

Last week, you've learnt how to setup a Database, pull data into a database, and query from it. There are some things that we haven't covered yet:

- dealing with large amounts of data
- transforming the data - your queries were used to display results, but were not stored or saved anywhere.

In this unit we will cover both of those points! We will cover:
- Build multiple layers of data quality:
  - a raw layer: the raw / un transformed data. The source data, essentially
  - a staging layer: an intermediate layer, where you'll do first pass of transformations on your data
    - converting types
    - renaming columns
    - converting timestamps etc
  - a mart layer: where you build new interesting tables/views, that could be used by business stakeholders, and where you calculate new fields and metrics.
- Setup DBT, which is a tool that enables you to structure a project around data transformations.
  - DBT knows where to create records in your data warehouse
  - Store all your SQL queries and configuration needed to build your new tables and views
