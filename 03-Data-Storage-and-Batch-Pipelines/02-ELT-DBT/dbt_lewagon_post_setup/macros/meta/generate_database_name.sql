{% macro generate_database_name(custom_database_name=none, node=none) -%}

    {{- log("Start generate_database_name macro") -}}
    {{- log("Initial default_database: " ~ target.database) -}}
    {{- log("node.fqn: " ~ node.fqn) -}}

    {%- set default_database = target.database -%}

    {%- if custom_database_name is none -%}
      {# Checking whether or not there is "mart" in the name of the parent folder #}
      {%- if node.fqn|length >=3 and node.fqn[1] == "mart" -%}

        {{- log("Length of the node greater than 3") -}}
        {%- set database = modules.re.sub("-stg", "-mart", default_database) -%}
        {{- log("New default_database: " ~ database) -}}

        {{ database }}

      {%- else -%}

        {{- log("Length of the node lower than 3") -}}
        {{ default_database }}
         {{- log("New default_database: " ~ default_database) -}}

      {%- endif -%}

    {%- else -%}

        {{- log("Custom Database is specified in the model") -}}
        {{ custom_database_name | trim }}

    {%- endif -%}

{%- endmacro %}
