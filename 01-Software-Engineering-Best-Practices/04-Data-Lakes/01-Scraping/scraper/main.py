import datetime as dt

from .scrape import scrape_hn


def main() -> None:
    """Scrape today's stories and save them to stories.csv."""
    today_str = dt.date.today().strftime("%Y-%m-%d")
    df = scrape_hn(today_str)
    df.to_csv("stories.csv", index=False)


if __name__ == "__main__":
    main()
