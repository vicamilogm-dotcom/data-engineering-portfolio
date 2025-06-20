with source as (
        select * from {{ source('sheets', 'Product_range') }}
  ),
  renamed as (
      select
        {{ adapter.quote("abv") }},
        {{ adapter.quote("name") }},
        {{ adapter.quote("size") }},
        {{ adapter.quote("base_unit") }},
        {{ adapter.quote("vendor_code") }},
        {{ adapter.quote("product_code") }},
        {{ adapter.quote("retail_price") }},
        {{ adapter.quote("country_of_origin") }}

      from source
  )
  select * from renamed
