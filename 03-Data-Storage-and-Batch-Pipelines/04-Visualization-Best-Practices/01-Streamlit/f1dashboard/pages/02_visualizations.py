"""
In data visualizations the following visualizations are shown:
- A bar chart with the top 5 drivers with the most points
- A line chart with the points of Lewis Hamilton over the years
"""

import altair as alt
import streamlit as st
from f1dashboard.advanced.state import F1State
from f1dashboard.advanced.queries import F1Queries
import pandas as pd


class DataVisualizations:
    def __init__(self) -> None:
        self.f1_state = F1State()
        self.f1_queries = F1Queries()

    def top_drivers(self):
        """Create a bar chart with the top 5 drivers"""

        st.subheader("Top 5 Drivers")
        # Use your package logic to load data, then plot it accordingly.
        pass  # YOUR CODE HERE

    def lewis_hamilton_over_the_years(self):
        """Create a line chart with the points of Lewis Hamilton over the years"""
        st.subheader("Lewis Hamilton over the years")

        # Use your package logic to load data, then plot it accordingly.
        pass  # YOUR CODE HERE


if __name__ == "__main__":
    st.title("Data visualizations")
    pass  # YOUR CODE HERE
