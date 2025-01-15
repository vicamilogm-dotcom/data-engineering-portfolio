"""
The page with the descriptive statistics allows a user of this dashboard
to get the summary statistics of the tables in the database.
"""
import streamlit as st
from f1dashboard.advanced.state import F1State
from f1dashboard.advanced.constants import F1Constants
from f1dashboard.advanced.database import F1Database
from f1dashboard.advanced.queries import F1Queries


class DescriptiveStatistics:
    def __init__(self) -> None:
        """Initialize the class"""
        self.f1_state = F1State()
        self.f1_database = F1Database()
        self.f1_queries = F1Queries()

    def select_table(self):
        """Select the table to explore"""
        with st.sidebar:
            st.subheader("Select table to explore")
            self.selected_table = "races"
            # TODO: REPLACE THIS LINE ABOVE BY A "st.selectbox" using F1Constants
            pass  # YOUR CODE HERE

    def summary_statistics(self):
        """st.write summary statistics of the selected dable"""
        st.title("Descriptive statistics")

        if self.selected_table in st.session_state:
            st.info(f"Retrieve the {self.selected_table} table from state...")
            pass  # YOUR CODE HERE
        else:
            st.info(f"Retrieve the {self.selected_table} table from the database...")
            pass  # YOUR CODE HERE
            st.info(f"Saving the {self.selected_table} table to state...")
            pass  # YOUR CODE HERE

        # TODO: describe the table_results data
        pass  # YOUR CODE HERE


if __name__ == "__main__":
    data_visualizations = DescriptiveStatistics()
    data_visualizations.select_table()
    data_visualizations.summary_statistics()
