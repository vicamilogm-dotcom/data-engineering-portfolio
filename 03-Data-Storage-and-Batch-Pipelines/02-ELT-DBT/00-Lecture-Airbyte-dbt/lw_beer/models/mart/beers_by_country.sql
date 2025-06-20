select country_of_origin,
    sum(amount) as total_amount,
    sum(profit) as total_profit,
    {{ profit_per_unit("sum(profit)", "sum(amount)") }} as profit_per_unit
from {{ ref('beers_country') }}
group by country_of_origin
    having country_of_origin is not null
order by total_profit desc
