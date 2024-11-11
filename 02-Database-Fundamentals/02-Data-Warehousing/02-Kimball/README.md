# 🎯 Goal

Now that we have done some preprocessing on our raw Adventure Works bicycle sales data, the goal of this challenge is to create a data warehouse following the the Kimball approach from those processed tables!

As a data engineer, you may be asked for input on schema design. Being able to engage with less technical stakeholders and interpret their needs to create a mart that suits their needs is a valuable skill. Your technical skills are being leveraged in designing and creating the mart so that the technical requirement and query complexity for end users is lower.

In this challenge we'll go through:
- Interpretting our business stakeholders needs
- Design the mart schema and create the queries to create the tables needed from the raw data
- Create queries to answer some basic business questions
- Create a coarser grained table for query optimisation

<br>

# 1️⃣ Designing the mart

###  Initial Request: Comprehensive Sales Analysis

**Business Stakeholder**: "We need a nuanced understanding of our sales metrics. Specifically, we want to know:
- Sales performance by group and by quarter.
- The impact of special offers on sales."

You now need to answer the following questions:

❓ Design Question: What are the key metrics and dimensions for this request?
❓ Design Question: What is the grain of the data mart?
❓ Design Question: What is the best way to model the data mart?

These types of questions are hard to answer alone, so take some time to discuss with your buddy and come up with a solution.

<details>
<summary markdown='span'>💡 One solution (feel free to follow your own design)</summary>

**Data Engineer's Action**: To tackle this request, you decide to create a sales-focused data mart. You identify the following dimension tables: `TerritoryDim`, `SpecialOfferDim`, and `DateDim`. Your central fact table is `Fact_Sales`, which holds the key metrics like `SalesAmount`, `Quantity`, and foreign keys to dimension tables for a first fact table. We normally want to go the finest grain possible, ie. item by item.

</details>

<br>

# 2️⃣ Building the mart

It's time to create the tables in your data mart. Start by creating a new BigQuery dataset called `sales_mart`.

You can create the tables through the SQL editor in the BigQuery console.

## 2.1. Build the tables

Write the query to create the fact and dimension tables that you designed in Section 1. Break it down into as many queries as you need.

## 2.2. Build the queries

If we've designed our mart following the Kimball approach, it should be relatively easy to answer business questions based on the facts and dimensions.

❓ Write a query to get the highest performing special offer in terms of sales amount


<details>
<summary markdown='span'>Answer for the best special offer</summary>

```bash
Volume Discount 11 to 14

4,896,451.9101781

0.02
```

</details>

❓ Write a query to get to get the best performing groups ordered by sales

<details>
<summary markdown='span'>Target Result</summary>

| Row | SalesGroup    | TotalSales          |
|-----|---------------|---------------------|
| 1   | North America | 79,353,361.16227    |
| 2   | Europe        | 19,837,684.27828    |
| 3   | Pacific       | 10,655,355.95931    |

</details>

<br>

# 3️⃣ Follow up requests

We find ourselves making lots of queries at a granularity of territory per month and we want to optimize our queries. We decide to create a new table that will be a snapshot of the sales per month and territory.

❓ Create a new fact table called `MonthlySalesSnapshotFact` that will be a snapshot of the sales per month and territory.

Why do we do this?

In the Kimball methodology for data warehousing, creating specialized fact tables like `MonthlySalesSnapshotFact` serves several purposes:

1. **Performance**: Aggregating data at the month and territory level allows for quicker query performance, reducing the need for on-the-fly aggregation of large datasets.

2. **Simplicity for End Users**: A pre-aggregated table at the monthly level makes it easier for business analysts to write queries without needing to group data themselves.

3. **Focused Metrics**: Creating a table that focuses on specific metrics (e.g., `MonthlySalesAmount` and `MonthlyQuantitySold`) simplifies the data model and makes it more understandable.

4. **Different Granularity**: The original `SalesOrderItemFact` table likely has a finer granularity (e.g., down to the individual order or item). A monthly snapshot table provides a different, coarser level of granularity useful for trend analysis.

5. **Data Consistency**: Pre-aggregated tables help ensure that everyone in the organization is working from the same numbers, reducing discrepancies that can arise from individual ad-hoc queries.

6. **Optimized Storage**: Storing pre-aggregated data can also optimize storage costs and computational resources, as you're storing fewer rows with just the metrics you need for specific types of analysis.

7. **Complex Queries**: Some types of analysis may require joining multiple tables or performing complex calculations. Having a pre-aggregated table can simplify these operations, making it easier to create reports and dashboards.

8. **Flexibility**: You can easily extend this table to include additional metrics or dimensions as the business requirements evolve, without affecting the existing data warehouse schema.

By creating a specialized table like `MonthlySalesSnapshotFact`, you align well with the Kimball methodology's focus on meeting specific business needs through tailored data structures.

<br>

# 4️⃣ (Optional) Snowflake Schema

Instead of setting up a star schema, you could attempt to model the data using a snowflake schema. This is a more complex schema but it can be more flexible and easier option to maintain. If you want to go even further, you could try to add another business unit and build a galaxy schema. The best way to understand data warehousing is to take the time to build one yourself - don't be afraid to make mistakes!

The Kimball group has a lot of resources on data warehousing and dimensional modeling. You can find them here:

https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/

<br>

# 🏁 Finish

Congratulations 🎉 you've created a data mart based on adventure works sales data!

You can save your queries that you used to create the tables and find the answers to the business questions, create `.sql` files in the challenge directory on your VM. There are no tests for this challenge, but don't forget to commit and push your code to github!

<br>
