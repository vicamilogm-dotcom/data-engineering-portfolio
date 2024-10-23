
# ELT and DBT lecture

## Setup an Airbyte instance

The legacy [airbyte oss](https://github.com/airbytehq/airbyte) docker compose setup using `./run-ab-platform.sh` demoed in the lecture has been deprecated

The [new setup](https://docs.airbyte.com/using-airbyte/getting-started/oss-quickstart) uses the dedicated `abctl` tool leveraging kubernetes

Here are the steps to install on the VM of the [data engineering setup](https://github.com/lewagon/data-engineering-setup)

1. Install

``` bash
sudo abctl local install
```

2. Port forward

8000 -> localhost:8000 to access airbyte locally

3. Retrieve password

``` bash
sudo abctl local credentials
```

4. Take down

The kubernetes instance can be brought down using:

``` bash
abctl local uninstall
```

## Setup an empty DBT project

``` bash
poetry init
poetry add dbt-core
poetry add dbt-bigquery
```

``` bash
poetry shell

dbt init
dbt run
```

# ELT and DBT recap options

Airbyte:
- Showcase the UI for the custom connector Builder allowing to connect REST APIs

VSCode:
- [Power User for DBT](https://marketplace.visualstudio.com/items?itemName=innoverio.vscode-dbt-power-user)

Packages:
- [dbt_date](https://hub.getdbt.com/calogica/dbt_date/latest/) allows to handle dates without having to deal with datawarehouse-specific syntax
- [dbt_expectations](https://hub.getdbt.com/calogica/dbt_expectations/latest/)
