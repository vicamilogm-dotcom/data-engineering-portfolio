<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W1D5/streamlit-logo.png" alt="drawing" width="300"/>

# 1️⃣ Set-up
<details>
<summary markdown='span'>❓ Instructions (expand me)</summary>

## 🎯 Goal
By the end of the setup, you should have a working stack using docker-compose (PostgreSQL, Streamlit) with the Formula 1 database loaded into PostgreSQL. You will be able to access the Streamlit app at http://localhost:8501.

<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W1D5/localhost8501.png" alt="drawing" width="600"/>

❓ **Copy the f1db.sql*** file from the previous challenge and copy it inside the `database/init` folder.


❓ **Read very carefully the `docker-compose-basic.yml`** file we've created for you.

💡 To connect a Streamlit app to the database, we need to create a secrets file to store our database credentials. This file, which is in the `.toml` format, is never committed to Git and should always be kept private and secure. Streamlit automatically loads and parses this file at runtime if it is in the correct location, similar to how an `.env` file is used.

❓ **In the `.streamlit` folder** there is an existing config file responsible for the configuration of a few key elements in Streamlit. In the same folder add a `secrets.toml` file with the required credentials to connect to the PostgresSQL instance
  ```toml
  [postgres]

  drivername = "postgresql"
  host = "database"
  port = 5432
  database = "f1db"
  username = "postgres"
  password = "postgres"
  ```

❓ **Run your app**
```bash
docker compose -f docker-compose-basic.yml up
```
☝️ Check your logs: the sql script `01-Streamlit/database/init/f1db.sql` should be executed at startup time.
☝️ Connect to DBEAVER to double-check (otherwise, execute it with the DBeaver interface)
☝️ You should be able to access the basic Streamlit app at http://localhost:8501.

</details>

---

# 2️⃣ Streamlit basics 😎

<details>
<summary markdown='span'>❓ Instructions (expand me)</summary>


🎯 We are going to use real Formula 1 data. The goal of this exercise is to get you familiar with the basic functionalities of Streamlit, while exploring the Formula 1 dataset 🚗.

📚 Use the [documentation](https://docs.streamlit.io/library/api-reference) of Streamlit to help you.

In the `f1dashboard` folder there is a file called `basic.py`. It is already partly filled with code, but your goal is to enhance the main Streamlit page with the following:

❓ Add the right caching decorator to the `load_data()` function. The `load_data` function loads the data from the database.
<details>
  <summary markdown='span'>🤯 Why?</summary>

🤯  The caching mechanism makes sure that the loaded data is stored in the `cache` of Streamlit. The next time that the Streamlit script is run, the data does not have to be retrieved from the database, but can be retrieved from `cache`, speeding up the application.
</details>

❓ Fill `create_main_page()` function to add more content!
- 💡 At the moment the `create_main_page()` function returns `races` as a string value. This value is used as input by the `load_data()` function to load the data. However, `races` is not the only table in the database. All table names are stored a list called `tables` (see the top of the `basic.py` file). Your job is to create a **[Streamlit selectbox widget](https://docs.streamlit.io/library/api-reference/widgets/st.selectbox)** that uses this list as its input, and allows the user to select one of the tables. Return the selected table from the `create_main_function`.

❓ Fill `summary_statistics` to explore the data and do some summary statistics on the data using the `describe()` method.
❓ Fill `top_drivers` that returns and shows the number of points for the 5 best-performing drivers in descending order using the `drivers` and `driver_standings` tables.
❓ Create a bar chart with these top_drivers under `if __name__ == '__main__':` using the plotting library of your choice (see [streamlit charts docs](https://docs.streamlit.io/library/api-reference/charts)):
- streamlit basic bar charts (`st.bar_chart`) - uses altair under the hood
- altair interactive (`st.altair_chart`)
- plotly interactive (`st.plotly_chart`)

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


<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W1D5/top_drivers.png" alt="drawing" width="300"/>


❓ Fill `lewis_over_the_years` and create a line chart with the number of points for the driver **Lewis Hamilton** over the years. You need the `drivers`, `driver_standings` and `races` table.

<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W1D5/lewis_over_the_years.png" alt="drawing" width="300"/>


❓ Fill `session_state()`. The data that is loaded needs to be stored into the [session state](https://docs.streamlit.io/library/api-reference/session-state) for it to be reusable across different pages in Streamlit. We'll need this for next sections.

💾  **Commit and push** your code when you are finished.✨

</details>

---

# 3️⃣ Multipage Streamlit in OOP 💪
<details>
<summary markdown='span'>❓ Instructions (expand me)</summary>

We have a basic Streamlit app now, which we have coded in a single python file. In order to make the app scalable and future-proof, we have some refactoring to do.

## `advanced.py`

❓ Copy and paste the contents of `docker-compose-basic.yml` to `docker-compose-advanced.yml`, but change the Streamlit file that you run from `"f1dashboard/basic.py"` to `"f1dashboard/advanced.py"`.

❓ Run `docker compose -f docker-compose-advanced.yml up`

❓ Understand your landing page logic.

We'll help you convert your basic application into a [multi-page app](https://blog.streamlit.io/introducing-multipage-apps/): In the `pages` folder there are two files. Each of these files create a separate page in the Streamlit app, which is visible in the sidebar. However, they can share the same `st.session_state` dictionary!

## `pages/01_descriptives.py`

❓ First, understand `__main__`, then `__init__` logic. You'll see that we've coded the app in OOP paradigm which implements *separation of concerns*
  - `database.py` - For initializing the database connection
  - `state.py` - Contains the session_state logic
  - `constants.py` - Contains the table names of the database

❓ Then, implement `select_table()`

❓ Then, implement `summary_statistics()`

❓ Convince yourself that we are indeed caching every raw tables we load to never load it twice


## `pages/02_visualizations.py`

❓ Try to move your two previous visualizations (`top_drivers` and `lewis_hamilton_over_the_years`) into this page, re-using the OOP approach as much as possible: *Separation of concerns* means that the only new real logic in "Visualization" class should be some *graph logic* such as `st.chart(...)`.

❓ Convince yourself that we are indeed saving to state every transformed dataframe we compute to never do it twice!

❓ Then, create a 3rd new visualization of your choice following the OOP pattern.


</details>

---

# 4️⃣ Storytelling 📢

<details>
<summary markdown='span'>❓ Instructions (expand me)</summary>

Now that the engineering structure is in place, it is time to explore the data further 📊. Pick a Formula 1 team of your choice, different from that of your buddy of the day. Your job will be to

❓ Give a **presentation** to your buddy at 5pm about how well you think your team will perform in 2019 based on data from previous years 📈.

❓ Your buddy is interested in learning about the *technical details* of your Streamlit application. Therefore, you should **create an extra page in your Streamlit app where you explain how you ensure that your web app stays fast**, even if the amount of data increases.

Some analytical questions that you could answer in your presentation include:

- ❓ How many points has your team scored over the years?
- ❓ Who are your current drivers?
- ❓ If a driver is not performing well, which drivers from other teams should
your team consider getting?
- ❓ What has historically been the best racetrack for your team? 👍
- ❓ What has been the worst racetrack? 👎
- ❓ Which two teams are your closest competitors? 💥

💡 Use your creativity to come up with additional analysis if you have time. Feel free to play with the `CSS` (see `.streamlit/config.toml`) as well to make your app look nicer! Support your analysis using Streamlit titles and text using Markdown. There is no need to create any slides for your presentation. No worries if you do not get to finish all the questions!

🚀 Good luck and enjoy!

</details>

---

### ⚙️ Bonus engineering challenge (no solutions given)
💡 Using Airflow to handle some data transformations might be a good idea. You could set up the dag to run on a schedule, like every 5 minutes, so that new data gets queried from the database as soon as it's available. Then, instead of the Streamlit app hitting the database for data, it can just read from the location where the Airflow results are stored. This can save time and make things run more smoothly, especially if you're constantly needing new data.
