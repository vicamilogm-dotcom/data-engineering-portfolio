
# ELT and DBT lecture

## Setup an Airbyte instance

The legacy [Airbyte oss](https://github.com/airbytehq/airbyte) 🔗 docker compose setup using `./run-ab-platform.sh` demo'ed in the lecture has been [deprecated](https://github.com/airbytehq/airbyte/discussions/40599) 🔗

The [new setup](https://docs.airbyte.com/using-airbyte/getting-started/oss-quickstart) 🔗 uses the dedicated `abctl` tool leveraging kubernetes.

Here are the steps to install on the VM of the [data engineering setup 🔗](https://github.com/lewagon/data-engineering-setup)

1. Install `abctl` with `curl`:
    ```bash
    # Remind students not to curl random bash scripts from the internet
    curl -LsfS https://get.airbyte.com | bash -
    ```

2. Create a local Airbyte instance:
    ```bash
    abctl local install
    ```

3. Port forward

    8000 -> localhost:8000 to access airbyte locally

4. Retrieve credentials for local instance
    ```bash
    abctl local credentials
    ```

5. Tear down local Airbyte kubernetes instance:
    ```bash
    abctl local uninstall
    ```

## Airbyte Data Source

Google sheet used in the lecture is available at this [link here 🔗](https://docs.google.com/spreadsheets/d/1zaNFq_18ZkWqVXyivDBFLdQAugVr8MFQwEA_1Br3iuk/edit?gid=2001955841#gid=2001955841)

- Copy the sheet to your own google account.
- Ideally make it private
- Share the sheet with the Service Account that you create for your **connector**

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

- Make sure to update the `project` field in the `profiles.yml`!

# More recap options

Airbyte:
- Showcase the UI for the custom connector Builder allowing to connect REST APIs

VSCode:
- [Power User for DBT](https://marketplace.visualstudio.com/items?itemName=innoverio.vscode-dbt-power-user) 🔗

Packages:
- [dbt_date](https://hub.getdbt.com/calogica/dbt_date/latest/) 🔗 allows to handle dates without having to deal with datawarehouse-specific syntax
- [dbt_expectations](https://hub.getdbt.com/calogica/dbt_expectations/latest/) 🔗
