{{ config(materialized='view') }}

with sales as (
    select
        orders_id,
        products_id,
        date_date,
        cast(revenue as numeric)  as revenue,
        cast(quantity as int64)   as quantity
    from {{ ref('stg_raw_sales') }}
),

product as (
    select
        products_id,
        cast(purchase_price as numeric) as purchase_price
    from {{ ref('stg_raw_product') }}
)

select
    s.products_id,
    s.orders_id,
    s.date_date,

    round(s.revenue, 2) as revenue,
    s.quantity,

    round(p.purchase_price, 2) as purchase_price,

    round(s.quantity * p.purchase_price, 2) as purchase_cost,
    round(s.revenue - (s.quantity * p.purchase_price), 2) as margin

from sales s
left join product p using (products_id)
order by orders_id desc
