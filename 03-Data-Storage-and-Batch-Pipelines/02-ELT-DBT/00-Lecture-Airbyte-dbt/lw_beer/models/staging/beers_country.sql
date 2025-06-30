{{ config(materialized="table") }}

select product_code,
    date_and_time_of_unloading,
    name,
    country_of_origin,
    base_unit,
    cast(amount as float64) as amount,
    cast(size as float64) as size,
    cast(sale_amount as float64) as sale_amount,
    cast(profit as float64) as profit
from {{ source('sheets', 'Product_range') }}
join {{ source('sheets', 'Transactions') }}
using (product_code)
