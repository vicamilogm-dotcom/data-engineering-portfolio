
# ELT and DBT lecture

## Setup an Airbyte instance

The legacy [Airbyte oss](https://github.com/airbytehq/airbyte) 🔗 docker compose setup using `./run-ab-platform.sh` demo'ed in the lecture has been [deprecated](https://github.com/airbytehq/airbyte/discussions/40599) 🔗

The [new setup](https://docs.airbyte.com/using-airbyte/getting-started/oss-quickstart) 🔗 uses the dedicated `abctl` tool leveraging kubernetes.

Here are the steps to install on the VM of the [data engineering setup](https://github.com/lewagon/data-engineering-setup) 🔗

1. Install `abctl`

    Using `curl`:

    ``` bash
    curl -LsfS https://get.airbyte.com | bash -
    ```

2. Install airbyte

    ``` bash
    sudo abctl local install
    ```

3. Port forward

    8000 -> localhost:8000 to access airbyte locally

4. Retrieve password

    ``` bash
    sudo abctl local credentials
    ```

5. Take down airbyte

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
- [Power User for DBT](https://marketplace.visualstudio.com/items?itemName=innoverio.vscode-dbt-power-user) 🔗

Packages:
- [dbt_date](https://hub.getdbt.com/calogica/dbt_date/latest/) 🔗 allows to handle dates without having to deal with datawarehouse-specific syntax
- [dbt_expectations](https://hub.getdbt.com/calogica/dbt_expectations/latest/) 🔗

DBT Deployment:
- Show how to create a new target for deployment
