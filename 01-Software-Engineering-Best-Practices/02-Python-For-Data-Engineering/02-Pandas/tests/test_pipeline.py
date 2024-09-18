import pandas as pd
import pathlib

DATA_PATH = pathlib.Path(__file__).parent.parent / "data"


def test_category_distribution_csv():
    category_df = pd.read_csv(DATA_PATH / "category_distribution.csv")
    assert list(category_df.columns) == ["category", "count"], "Columns mismatch"
    assert not category_df.isnull().any().any(), "Found null values"
    assert category_df["count"].sum() > 0, "Sum of counts is zero or negative"
    assert (
        category_df.loc[category_df["category"] == "Fiction", "count"].iloc[0] == 824439
    ), "Count for Fiction is incorrect"


def test_best_performing_books_csv():
    best_books_df = pd.read_csv(DATA_PATH / "best_performing_books.csv")
    assert list(best_books_df.columns) == [
        "title",
        "average_review_score",
        "number_of_reviews",
        "author",
    ], "Columns mismatch"
    assert len(best_books_df) == 10, "Number of entries is not 10"
    assert (
        best_books_df["number_of_reviews"].min() >= 25
    ), "Minimum reviews is less than 25"
    assert (
        best_books_df.loc[0, "title"]
        == "A Reason To Live : The True Story of One Woman's Love, Courage and Determination to Survive"
    ), "Title at index 0 is incorrect"


def test_author_impact_analysis_csv():
    author_df = pd.read_csv(DATA_PATH / "author_impact_analysis.csv")
    assert list(author_df.columns) == [
        "author",
        "average_review_score",
        "number_of_reviews",
        "impact_score",
    ], "Columns mismatch"
    assert not author_df.isnull().any().any(), "Found null values"
    assert len(author_df) == 10, "Number of entries is not 10"
    assert (
        not author_df["author"].str.contains(r"[\[\]]").any()
    ), "Brackets found in author names"
    assert author_df.loc[0, "author"] == "Jane Austen", "Author at index 0 is incorrect"


def test_review_years_csv():
    review_years_df = pd.read_csv(DATA_PATH / "review_scores_over_time.csv")
    assert list(review_years_df.columns) == [
        "review_year",
        "review/score",
    ], "Columns mismatch"
    assert not review_years_df.isnull().any().any(), "Found null values"
    assert (
        review_years_df["review_year"].dtype == "int64"
    ), "review_year data type mismatch"
    assert (
        review_years_df["review/score"].dtype == "float64"
    ), "review/score data type mismatch"
    assert (
        review_years_df.loc[
            review_years_df["review_year"] == 1996, "review/score"
        ].iloc[0]
        == 4.639289678135405
    ), "Review score for 1996 is incorrect"
