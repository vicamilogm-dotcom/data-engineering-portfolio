# 🎯 Goals

- Sync dags from a repo to the airflow server
- Update syntax

<br>

# 1️⃣ Move the dags to a repo

1. Copy the dag folder outside of data engineering challenges and create a new repo with them in!

1. Generate a Personal Authorization Token (PAT) with permission to the repo you created!
    1. Go to [github.com](https://www.github.com)
    1. Click your icon in the top right
    1. Click **Settings** in the right pop-out menu
    1. In the left menu all the way at the bottom click on **Developer Settings**
    1. Select **Personal access tokens** --> **Fine-grained tokens**
    1. Click **Generate new token** in the top right
        1. Give your token a name, something descriptive
        1. You can select the repository access, for example only select repositories --> the repository you just created
        1. Change the **Repository permissions** of **Contents** to Access: Read-only. This will also change the **Metadata** permission, a dependency of **Contents**.
        1. Select **Generate token** at the bottom of the page
        1. Make sure you copy the token key to your clipboard! You only get one chance to copy it! Put it in your `.env` file.

1. Update the docker-compose.yml to include the new repo and checkout the changes

1. In the **Recap** directory. Create a folder for your synced dags to land in and change the permissions:
    ```bash
    mkdir -p ./git-dags
    sudo chmod -R 777 ./git-dags
    ```

1. Run the compose

1. Add a new DAG to the repo and see it appear in the Airflow server after a while! It might take a few minutes.

```python
from datetime import datetime, timedelta
from airflow import DAG
from airflow.decorators import task, dag

@dag(schedule_interval='@daily', start_date=datetime(2022, 1, 1), catchup=False)
def complex_taskflow():

    @task()
    def extract():
        return {'data': 42}

    @task()
    def transform(order_data_dict: dict):
        return {'data': order_data_dict['data'] * 2}

    @task()
    def load(total_order_value: dict):
        print(f"Total order value is: {total_order_value['data']}")

    @task(multiple_outputs=True)
    def branch():
        return {
            'branch_a': 'Branch A data',
            'branch_b': 'Branch B data',
        }

    @task()
    def end():
        print('End task')

    order_data = extract()
    order_summary = transform(order_data)

    branch_data = branch()
    load(order_summary)

    end1 = end()
    end2 = end()

    order_summary >> [end1, end2]
    branch_data['branch_a'] >> end1
    branch_data['branch_b'] >> end2

example_dag = complex_taskflow()
```

❓ Explore the `git-dags` directory to understand the structure and how files are being passed around containers.

A great way to de-couple your development of DAGs from your production environment. While it can take a few minutes for dags to synchronize (and even longer if you delete a DAG), if you're cutting things that fine that you need to run a DAG immediately, you probably have bigger problems than a DAG being a few minutes late.

<br>

# 2️⃣ Airflow Taskflow Syntax

1. What is the syntax of the above DAG?

    https://airflow.apache.org/docs/apache-airflow/stable/tutorial/taskflow.html

1. As a class work though migrating transform.py to the new syntax!

<br>
