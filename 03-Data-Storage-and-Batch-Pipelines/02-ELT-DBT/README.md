## Prerequisites

Make sure you've
- Enabled the BigQuery API and can run `gcloud` commands in your terminal

## Recap from last module and high level view of the unit

Last unit, you've learnt how to setup a Database, pull data into a database, and query from it. There are some things that we haven't covered yet:
- Dealing with large amounts of data
- Transforming data - your queries were used to display results, but were not stored or saved anywhere.

In this unit we will cover both of those points! We will cover:
- Build multiple layers of data quality:
  - Raw layer: the raw, untransformed source data.
  - Staging layer: an intermediate layer, where you'll do a first pass of transformations on your data
    - Casting types
    - Renaming columns
    - Dropping redundant columns
  - Intermediate layer: with trnasformations and aggregations
  - Mart layer: where you build new interesting tables/views, that could be used by business stakeholders, and where you calculate new fields and metrics.
- Setup DBT, which is a tool that enables you to structure a project around data transformations.
  - DBT knows where to create records in your data warehouse
  - Store all your SQL queries and configuration needed to build your new tables and views
