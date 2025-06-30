select country_of_origin,
    sum(amount) as total_amount,
    sum(profit) as total_profit,
    {{ amount_per_unit('sum(profit)', 'sum(amount)') }} as profit_per_unit
-- Don't forget to update with your project_id
-- from `<your_project_id>`.`lw_beer`.`beers_country`
from {{ ref('beers_country') }}
group by country_of_origin
    having country_of_origin is not null
order by total_profit desc
