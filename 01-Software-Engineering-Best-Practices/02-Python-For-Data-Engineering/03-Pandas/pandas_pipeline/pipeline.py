import pathlib

from pandas_pipeline.load import load_data
from pandas_pipeline.best_books import write_best_performing_books
from pandas_pipeline.category_distribution import write_category_distribution
from pandas_pipeline.top_authors import write_author_impact_analysis
from pandas_pipeline.review_years import write_review_scores_over_time


def pipeline(data_path: pathlib.Path):
    print("Starting pipeline...\n")

    print("Loading Data from CSV...\n")
    combined_df = load_data(data_path)

    print("Figuring out the worlds best books...\n")
    write_best_performing_books(combined_df, data_path)

    print("Calculating how books are distributed...\n")
    write_category_distribution(combined_df, data_path)

    print("Analysing author impact...\n")
    write_author_impact_analysis(combined_df, data_path)

    print("Processing review scores over time...\n")
    write_review_scores_over_time(combined_df, data_path)

    print("✅ Pipeline complete!\n")


if __name__ == "__main__":
    data_path = pathlib.Path(__file__).parent.parent / "data"
    pipeline(data_path)
