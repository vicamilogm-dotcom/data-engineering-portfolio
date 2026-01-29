{{ config(materialized='view') }}

with orders as (
    select
        date_date,
        orders_id,

        cast(quantity as int64)             as quantity,
        cast(revenue as numeric)            as revenue,
        cast(purchase_cost as numeric)      as purchase_cost,
        cast(margin as numeric)             as margin,
        cast(operational_margin as numeric) as operational_margin,
        cast(shipping_fee as numeric)       as shipping_fee,
        cast(log_cost as numeric)           as log_cost,
        cast(ship_cost as numeric)          as ship_cost
    from {{ ref('int_orders_operational') }}
),

daily as (
    select
        date_date,
        count(orders_id) as nb_transactions,
        sum(quantity) as quantity,

        sum(revenue) as revenue,
        sum(purchase_cost) as purchase_cost,
        sum(margin) as margin,
        sum(operational_margin) as operational_margin,

        sum(shipping_fee) as shipping_fee,
        sum(log_cost) as log_cost,
        sum(ship_cost) as ship_cost
    from orders
    group by date_date
)

select
    date_date,
    nb_transactions,
    quantity,

    round(revenue, 2) as revenue,
    round(safe_divide(revenue, nb_transactions), 2) as average_basket,

    round(margin, 2) as margin,
    round(operational_margin, 2) as operational_margin,
    round(purchase_cost, 2) as purchase_cost,

    round(shipping_fee, 2) as shipping_fee,
    round(log_cost, 2) as log_cost,
    round(ship_cost, 2) as ship_cost
from daily
order by date_date desc
