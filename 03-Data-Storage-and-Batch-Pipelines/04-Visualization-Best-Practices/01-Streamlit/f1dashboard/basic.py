import altair as alt
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from timeit import default_timer as timer


conn_string = URL.create(**st.secrets["postgres"])
conn = create_engine(conn_string, echo=False)
TABLES = [
    "races",
    "circuits",
    "constructor_results",
    "constructor_standings",
    "constructors",
    "driver_standings",
    "drivers",
    "lap_times",
    "pit_stops",
    "qualifying",
    "results",
    "seasons",
    "status",
]


pass  # YOUR CODE HERE
def load_data(table_name):
    """
    Loads the races data from the F1 database.
    Implement the right caching decorator.
    Returns:
        pd.DataFrame: The race dataset
    """
    data = pd.read_sql_query(f"select * from {table_name}", conn)

    return data


def create_main_page():
    """
    Creates the following Streamlit headers:
    - A title
    - A subheader
    - A title in the sidebar
    - A markdown section in the sidebar
    - A widget in the sidebar to select a table from the `TABLES` list,
    and then return the selected table (instead of the hard-coded "races" value)
    """
    st.title("Formula 1 Dashboard")
    st.info(
        """
    Delete me once completed
    """
    )
    selected_table = "races"

    pass  # YOUR CODE HERE
    return selected_table


def summary_statistics(data):
    """
    Creates a subheader and writes the summary statistics for the data
    """
    st.subheader("Summary statistics")
    st.info("Use the describe method to get the summary statistics")
    pass  # YOUR CODE HERE


@st.cache_data
def top_drivers():
    """
    Get the top 5 drivers with the most points.
    You can get the name from the drivers table and
    combine it with the points from the driver_standings table.
    Returns:
        pd.DataFrame: The top 5 drivers with the columns:
                      - driver_name
                      - total_points
    """
    st.info("Write a query to get the top 5 drivers and visualize the results.")
    pass  # YOUR CODE HERE


@st.cache_data
def lewis_over_the_years():
    """
    Get the points from Lewis Hamilton between 2007 and 2018.
    Use the following table to get the data:
        - drivers
        - driver_standings
        - races

    Returns:
        pd.DataFrame: The points from Lewis Hamilton over the years, with the columns:
                        - year
                        - total_points
    """
    st.info(
        "Write a query to get the points of Lewis Hamilton over the years and visualize the results."
    )
    pass  # YOUR CODE HERE


def session_state(data):
    """
    Initialize the session state
    using data as the key and value as the
    initialization value.

    Put data in the session state after having
    initialized it.

    Args:
        data (pd.DataFrame): The formula 1 dataset
    """

    # Initialization of session state, assign a random value
    # to the session state
    pass  # YOUR CODE HERE

    # Update the session state using the dataframe
    pass  # YOUR CODE HERE


if __name__ == "__main__":
    selected_table = create_main_page()

    # used to time the loading of the data
    start = timer()
    data = load_data(selected_table)
    end = timer()
    st.sidebar.info(f"{round(end-start,4)} seconds to load the data")

    st.dataframe(data)

    summary_statistics(data)
    session_state(data)

    st.subheader("Top 5 Drivers")
    top_driver_data = top_drivers()
    st.write(top_driver_data)
    st.warning("Use the Altair library to create a bar chart with the top drivers")
    # create a bar chart with the top drivers
    pass  # YOUR CODE HERE

    st.subheader("Lewis Hamilton over the years")
    lewis_years = lewis_over_the_years()

    # Convert the year column to datetime
    lewis_years["year"] = pd.to_datetime(lewis_years["year"], format="%Y")

    st.warning("Create a line chart with the lewis_years, use the Altair library")
    pass  # YOUR CODE HERE
