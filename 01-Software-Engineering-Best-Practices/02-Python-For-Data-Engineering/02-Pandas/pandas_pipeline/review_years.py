import pandas as pd
from pathlib import Path


def write_review_scores_over_time(ratings_df, data_path: Path) -> None:
    """
    Calculate the average review scores over time and save the result to a CSV file.

    Parameters:
    - ratings_df (pd.DataFrame): DataFrame containing the columns 'review/score' and 'review/time'.
    - data_path (pathlib.Path): The path where the output CSV will be saved.

    Output File:
    - "review_scores_over_time.csv" saved in the specified `data_path`.

    Output Columns:
    - review_year: The year when the review was made.
    - review/score: The average review score for that year.

    Returns:
    - None. Outputs a CSV file named 'review_scores_over_time.csv' in the specified directory.
    """
    pass  # YOUR CODE HERE
