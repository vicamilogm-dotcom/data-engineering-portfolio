with source as (
        select * from {{ source('sheets', 'Transactions') }}
  ),
  renamed as (
      select
        cast({{ adapter.quote("amount") }} as float64) as amount,
        cast({{ adapter.quote("profit") }} as float64) as profit,
        cast({{ adapter.quote("sale_amount") }} as float64) as sale_amount,
        {{ adapter.quote("product_code") }},
        cast({{ adapter.quote("discount_amount") }} as float64) as discount_amount,
        cast({{ adapter.quote("percentage_markup") }} as float64) as percentage_markup,
        cast({{ adapter.quote("discount_percentage") }} as float64) as discount_percentage,
        {{ adapter.quote("date_and_time_of_unloading") }}

      from source
  )
  select * from renamed
