{{ config(materialized='view') }}

with orders_margin as (
    select
        orders_id,
        date_date,
        cast(revenue as numeric)        as revenue,
        cast(quantity as int64)         as quantity,
        cast(purchase_cost as numeric)  as purchase_cost,
        cast(margin as numeric)         as margin
    from {{ ref('int_orders_margin') }}
),

ship as (
    select
        orders_id,
        cast(shipping_fee as numeric) as shipping_fee,
        cast(log_cost as numeric)     as log_cost,
        cast(ship_cost as numeric)    as ship_cost
    from {{ ref('stg_raw_ship') }}
)

select
    om.orders_id,
    om.date_date,

    round((om.margin + s.shipping_fee) - (s.log_cost + s.ship_cost), 2) as operational_margin,

    om.quantity,
    round(om.revenue, 2)        as revenue,
    round(om.purchase_cost, 2)  as purchase_cost,
    round(om.margin, 2)         as margin,

    round(s.shipping_fee, 2) as shipping_fee,
    round(s.log_cost, 2)     as log_cost,
    round(s.ship_cost, 2)    as ship_cost

from orders_margin om
left join ship s
    on om.orders_id = s.orders_id
order by om.orders_id desc
