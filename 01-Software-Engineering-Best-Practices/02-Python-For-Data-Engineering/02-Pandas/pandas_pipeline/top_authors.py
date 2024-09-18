import pandas as pd
from pathlib import Path


def write_author_impact_analysis(combined_df: pd.DataFrame, data_path: Path) -> None:
    """
    Generates a CSV file of the top 10 most impactful authors based on their average review score and number of reviews.

    Criteria:
    - Impact is calculated as a weighted sum of normalized review scores and normalized number of reviews.
    - The weighting for number of reviews is 0.8.
    - Missing authors are not considered in the analysis.
    - Brackets around author names are removed in the output.

    Parameters:
    - combined_df (pd.DataFrame): DataFrame resulting from the merge of ratings and book details.
    - data_path (Path): pathlib.Path object indicating where the result should be saved.

    Output File:
    - "author_impact_analysis.csv" saved in the specified `data_path`.

    Output Columns:
    - author: The name of the author.
    - average_review_score: The average score of reviews received by the author's books.
    - number_of_reviews: The total number of reviews received by the author's books.
    - impact_score: Calculated score based on normalized review scores and number of reviews (with a 0.8 weighting on reviews).

    Returns:
    - None: Writes the result to the specified path.
    """
    pass  # YOUR CODE HERE
