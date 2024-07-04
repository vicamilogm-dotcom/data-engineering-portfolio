# 🎯 Goal

So now we have a data mart. Next step is to give an end user, like an analyst, access to the data. But in this challenge, we are going to make sure we have good data and access hygiene by applying the [principle of least privilege](https://en.wikipedia.org/wiki/Principle_of_least_privilege).

We've identified that an analyst needs some data to build a dashboard that is updated daily for high level business monitoring, but they do not require access to any of the other tables. Your goal is to create a new *view* in the data warehouse, and then configure the Identity and Access Management (IAM) permissions so that they only have access to that view.

<br>

# 1️⃣ Create a BigQuery view

Imagine that the our underlying data is updated frequently, but we want to maintain a simplified object for our analysts to work. A view can be used, they do not store any data themselves like a table does, only the SQL query that defines the view. Each time a view is queried, BigQuery executes the underlying SQL in real time. This means that the performance of querying a view depends on the complexity and efficiency of the underlying query and the amount of data it processes.

The benefit is the underlying query can be highly optimised to minimize cost, but presents as a table like object. So less technical end users don't have to interact with the (potentially complex) query that created the view, but can easily query the view like they would any other table!

❓ Create a view called `AnalystSalesView`

1. **Sales Performance**: Details like `OrderQty`, `UnitPrice`, and `LineTotal` help in analyzing the revenue streams.
2. **Promotion Effectiveness**: By including `SpecialOfferDescription` and `SpecialOfferDiscount`, analysts can measure the impact of various promotions on sales.
3. **Temporal Trends**: The sales date and year (`SalesOrderDate`, `SalesOrderYear`) enable trend analysis over time.
4. **Regional Analysis**: The inclusion of `TerritoryName`, `TerritoryCountry`, and `TerritoryGroup` allows for region-specific sales analysis.

Now that the view has been created, it's time to configure IAM permissions.

<br>

# 2️⃣ BigQuery Identity and Access Management (IAM) Permissions

To provide analysts with permission to query this view in GCP, you can set up IAM roles in Google Cloud Platform. You can grant the role of `roles/bigquery.dataViewer` specifically for the dataset and the view.

❓ Look up how to do this in the [GCP documentation](https://cloud.google.com/bigquery/docs/dataset-access-controls#bigquery-dataset-iam-roles) and do it either via the `gcloud` CLI tool or console to give access to a class mate.

Check that they can query your view and nothing else!

<br>

# 3️⃣ Minimizing costs

The data that the analysts are using are currently stored as a BigQuery [view](https://cloud.google.com/bigquery/docs/views). We recieved feedback that management only need the data on a daily granularity level and don't need to include the current days data in their dashboard.

❓ What changes could be made to the view to minimize on costs?

<details>
<summary markdown='span'>🎁 Answer</summary>

We can make it into a [materialized view](https://cloud.google.com/bigquery/docs/materialized-views-intro) and schedule it to refresh overnight everyday!

Have a read on the differences between views and materialised views and try and understand how it could save on processing costs!

</details>

❓ First create the materialized view by having a look at the [documentation](https://cloud.google.com/bigquery/docs/materialized-views-create).


❓ Create a scheduled query to refresh the view every night at 3am

<details>
<summary markdown='span'>🎁 Refresh query</summary>

```sql
ALTER MATERIALIZED VIEW sales_mart.AnalystMaterializedView
REFRESH;
```
</details>

<br>

# 🏁 Finish

Congratulations on finishing this challenge! You've created a view and restricted access to it.

You can save your queries that you used to create the tables and find the answers to the business questions, create `.sql` files in the challenge directory on your VM. There are no tests for this challenge, but don't forget to commit and push your code to github!

<br>
