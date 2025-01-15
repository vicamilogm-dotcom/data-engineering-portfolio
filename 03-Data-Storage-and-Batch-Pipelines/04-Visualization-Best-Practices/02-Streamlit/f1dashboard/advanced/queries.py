import pandas as pd
import streamlit as st
from f1dashboard.advanced.database import F1Database


class F1Queries:
    def __init__(self) -> None:
        self.conn = F1Database().db_connection

    # # Perform query.
    # # Uses st.experimental_memo to only rerun when the query changes or after 10 min.
    @st.cache_data(ttl=600)
    def _run_query(_self, query):
        """
        Base utility method queries a database using pandas and returning a dataframe

        Parameters
        ----------
        query: Str
            SQL query as a f-string

        Returns
        -------
        races: pandas.DataFrame
            Dataframe containing the result of the query

        """

        return pd.read_sql_query(query, _self.conn)

    def retrieve_table(self, table_name):
        table_results = self._run_query(
            f"""
        select
            *
        FROM
            {table_name}
        """
        )
        return table_results

    def top_drivers(self):
        """
        Get the top 5 drivers with the most points.
        You can get the name from the drivers table and
        combine it with the points from the driver_standings table.
        Returns:
            pd.DataFrame: The top 5 drivers with the columns:
                        - driver_name
                        - total_points
        """

        pass  # YOUR CODE HERE
        return top_drivers

    def lewis_over_the_years(self):
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
        pass  # YOUR CODE HERE
        return lewis_points


if __name__ == "__main__":
    queries = F1Queries()
