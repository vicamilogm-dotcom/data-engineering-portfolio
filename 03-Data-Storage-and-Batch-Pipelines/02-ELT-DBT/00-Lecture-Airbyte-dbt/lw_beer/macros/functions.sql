{% macro profit_per_unit(amount, units) %}
    round({{amount}} / {{units}}, 2)
{% endmacro %}
