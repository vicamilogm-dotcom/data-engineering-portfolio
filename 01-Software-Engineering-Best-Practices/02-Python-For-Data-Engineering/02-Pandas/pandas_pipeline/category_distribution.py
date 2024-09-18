import pandas as pd
from pathlib import Path


def write_category_distribution(combined_df: pd.DataFrame, data_path: Path) -> None:
    """
    Generates a CSV file of the book categories distribution.

    Criteria:
    - Categories with a proportion less than 1% of the total count will be grouped into the "Other" category.
    - Removes any surrounding brackets from the category names.
    - The column names in the output will be lowercase.

    Parameters:
    - combined_df (pd.DataFrame): DataFrame resulting from the merge of ratings and book details.
    - data_path (Path): pathlib.Path object indicating where the result should be saved.

    Output File:
    - "category_distribution.csv" saved in the specified `data_path`.

    Output Columns:
    - category: The name of the book category, with any surrounding brackets removed.
    - count: The number of books in that category.

    Returns:
    - None: Writes the result to the specified path.
    """
    pass  # YOUR CODE HERE
