# 🎯 Goal

Streamlit is a popular open source framework that makes it quick and easy to get a web app up in a short amount of time. It only requires python to use, is incredibly quick to prototype, and is great for stateless web apps, either internally or externally facing.

In this challenge we'll go through:
- Setting up the docker compose stack for getting a Streamlit app running while connected to a database.
- Creating a simple page app in Streamlit.
- Creating a more complex, multi-page Streamlit app using OOP.
- Work with your buddy to expand the dashboard and present to your peers!

<br>

# 1️⃣ Setup

By the end of this section, you will have a working docker-compose stack with the Formula 1 data loaded into postgres, and be able to access the Streamlit app in your browser at http://localhost:8501. When you get there, it should look similar to the below:

<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W1D5/localhost8501.png" alt="Screenshot of streamlit dashboard after setup" width="600"/>

## 1.1. Data and Database Connection

Copy the `f1db.sql` file from the previous challenge and copy it inside the `database/init` directory. We do not need the `create_f1db.sql` script because we have set different environment variables.

Read the `docker-compose-basic.yml` file that has been provided.

💡 To connect a Streamlit app to the database, we need to create a secrets file to store our database credentials. This file, in `.toml` format, and like any secrets file, is never committed to Git and should always be kept private and secure. Streamlit loads and parses all files in `.streamlit/` at runtime.

❓ In the `.streamlit` directory there is an existing `config.toml` file responsible for the configuration of some elements in Streamlit. In the same directory add a `secrets.toml` file with the below credentials to connect to the PostgresSQL instance:

```toml
[postgres]

drivername = "postgresql"
host = "database"
port = 5432
database = "f1db"
username = "postgres"
password = "the-same-password-in-.env"
```

When you think you have the secrets configured, launch your app:

```bash
docker compose -f docker-compose-basic.yml up
```

To check that everything is working as intended:
- You should be able to access the Streamlit app at http://localhost:8501
- Connect your postgres container to DBeaver on your local computer and query one of the tables.
- Check your logs: the SQL script `01-Streamlit/database/init/f1db.sql` should be executed at startup time.

<br>

# 2️⃣ Streamlit Basics

In this section, you'll get familiar with the basic functionalities of Streamlit, while exploring the Formula 1 dataset 🏎️

📚 Use Streamlit's documentation at [this link](https://docs.streamlit.io/library/api-reference) if you need a reference. It's comprehensive, detailed, and easy to follow.


In the `f1dashboard` directory there is a file called `basic.py`. It is already partly filled, your goal is to enhance the main Streamlit page! Read the provided code carefully to see how it's formatted - similar to any other python file. The logic is defined in functions to load data, create visualisations, and define the layout of the app, then those functions are called in the `if __name__ == '__main__'` block.

## 2.1. Table Selection

Complete `create_main_page()` function to add more content!

💡 At the moment the `create_main_page()` function returns `races` as a string value. This value is used as input by the `load_data()` function to load the data. However, `races` is not the only table in the database. All table names are stored in a list called `TABLES`, declared at the top of `basic.py`.

Your job is to create a **[Streamlit selectbox widget](https://docs.streamlit.io/library/api-reference/widgets/st.selectbox)** in the [sidebar](https://docs.streamlit.io/develop/api-reference/layout/st.sidebar) that uses this list as its input, and allows the user to select one of the tables. `create_main_page` should return the selected table as a string.

## 2.2. Caching loaded data

Add the right caching decorator to the `load_data()` function. The `load_data` function loads the data from the database.

Play around with selecting new tables and see the difference in loading time between loading a table for the first time and then reloading it!

<details>
<summary markdown='span'>💡 Why?</summary>

Streamlit can `cache` data loaded from the database, so the next time the Streamlit script is run, the data does not have to be sourced from the database, but from cache, speeding everything up!
</details>

## 2.3. Summary Statistics

Complete the `summary_statistics` function to explore the data and do some summary statistics on the data using the `describe()` method. Streamlit might not have a built in method, but it can integrate with another popular data manipulation library!

💡 Think if the function needs to render data, or return data.

## 2.4. Top Drivers

Complete the `top_drivers` function that returns and shows the number of points for the 5 best performing drivers in descending order using the `drivers` and `driver_standings` tables.

📊 Create a bar chart with these top_drivers under `if __name__ == '__main__':` using the plotting library of your choice (see [streamlit charts docs](https://docs.streamlit.io/library/api-reference/charts)):
- Streamlit basic bar charts (`st.bar_chart`) - uses altair under the hood
- Altair interactive (`st.altair_chart`)
- Plotly interactive (`st.plotly_chart`)

<details>
<summary markdown='span'>🎁 Fancy altair syntax for the lazy!</summary>

```python
import altair as alt

bar_chart = alt.Chart(top_driver_data).mark_bar().encode(
    y=alt.Y("total_points"), x=alt.X("driver_name", sort="-y"),
    color="driver_name", tooltip="total_points"
    )

st.altair_chart(bar_chart, use_container_width=True)
```
</details>

<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W1D5/top_drivers.png" alt="drawing" width="450"/>

## 2.5. Lewis over the years

📈 Complete the `lewis_over_the_years` function and create a line chart with the number of points for the driver **Lewis Hamilton** over the years. You need the `drivers`, `driver_standings`, and `races` table.

💡 Be careful, the points in `driver_standings` are the cumulative points for the year for a given `driver_id` after the race was completed, not the points awarded for that specific race!

<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W1D5/lewis_over_the_years_correct.png" alt="drawing" width="450"/>

## 2.6. Statefullness with Session State

Fill `session_state()`. The data that is loaded needs to be stored into the [session state](https://docs.streamlit.io/library/api-reference/session-state) for it to be reusable across different pages in Streamlit. We'll need this for next section.

🧪 There are no tests for this section of the challenge, but make sure to git add, commit and push your code to github when you are finished.

<br>

# 3️⃣ Multi-page Streamlit with OOP

We have a basic Streamlit app now 💪 Which we have coded in a single python file. In order to make the app scalable and future-proof, we have some refactoring to do.

We'll help you convert your basic application into a [multi-page app](https://blog.streamlit.io/introducing-multipage-apps/). `advanced.py` will be the new entrypoint and landing page to your Streamlit app. In the `pages` directory there are two files. Each of these files create a separate page, visible in the sidebar. However, they can share the same `st.session_state` dictionary!

## 3.1. `advanced.py`

Copy and paste the contents of `docker-compose-basic.yml` to `docker-compose-advanced.yml`, but change the Streamlit file that you run from `"f1dashboard/basic.py"` to `"f1dashboard/advanced.py"`.

Make sure to tear down your basic app:

```bash
docker compose -f docker-compose-basic.yml down
```

Then launch your new app:

```bash
docker compose -f docker-compose-advanced.yml up
```

Have a look at the landing page and compare against the code in `advanced.py` to understand how it's working.

## 3.2. `pages/01_descriptives.py`

First, understand `__main__`, then `__init__` logic. You'll see that we've coded the app in OOP paradigm which implements *separation of concerns*
- `database.py` - For initializing the database connection
- `state.py` - Contains the session_state logic
- `constants.py` - Contains the table names of the database
- `queries.py` - SQL Queries for retrieving data from the database

❓ In `01_descriptives.py` implement:
1. `select_table()`
1. `summary_statistics()`

Load some data from different tables and convince yourself that we are indeed caching raw data so we never have load it from the database twice!

## 3.3. `pages/02_visualizations.py`

Move your two previous visualizations: `top_drivers` and `lewis_hamilton_over_the_years` into this page, re-using the OOP approach as much as possible.

*Separation of concerns* means that the only new real logic in the `DataVisualization` class should be some *graph logic* such as `st.chart(...)`.

Again, convince yourself that we are indeed saving the state of every transformed dataframe we compute to never do it twice!

Then, create a 3rd new visualization of your choice following the OOP pattern.

🧪 There are no tests for this section of the challenge, but don't forget to git add, commit, and push your code to Github!

<br>

# 4️⃣ Storytelling

Now that the engineering structure is in place, it is time to explore the data further 📊

As a pair with your buddy, pick a Formula 1 team of your choice. Your job will be to:

- Give a **presentation** to your group at the end of the session about how well you think your team will perform in 2019 based on data from previous years 📈.

- Your group is interested in learning about the *technical details* of your Streamlit application. Therefore, you should **create an extra page in your Streamlit app where you explain how you ensure that your web app stays fast**, even if the amount of data increases.

Some analytical questions that you could answer in your presentation include:

- ❓ How many points has your team scored over the years?
- ❓ Who are your current drivers?
- ❓ If a driver is not performing well, which drivers from other teams should
your team consider getting?
- ❓ What has historically been the best racetrack for your team? 👍
- ❓ What has been the worst racetrack? 👎
- ❓ Which two teams are your closest competitors? 💥

💡 Use your creativity to come up with additional analysis if you have time. Feel free to play with the `CSS` (see `.streamlit/config.toml`) as well to customise your app! Support your analysis using Streamlit titles and text using Markdown. There is no need to create any slides for your presentation. Don't stress if you do not get to finish all the questions!

🚀 Good luck and enjoy!

<br>
