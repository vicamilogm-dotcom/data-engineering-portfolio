import requests
from bs4 import BeautifulSoup
import pandas as pd


def scrape_hn(date: str) -> pd.DataFrame:
    """
    Scrape the daily top stories from Hacker News (HN) for a specified date.

    Parameters:
    - date (str): The desired date for which to scrape the top stories.
                  Format should be "YYYY-MM-DD".

    Returns:
    - pd.DataFrame: A DataFrame containing details of the top stories including:
        - rank (int): The ranking of the story on HN.
        - title (str): The title of the story.
        - site (str): The site domain from where the story is sourced.
        - link (str): The direct link to the story.
        - score (int): The total score (or upvotes) the story has received.
        - author (str): The name of the user who posted the story.
        - comments_number (int): The number of comments the story has.
                                Defaults to 0 if not present.

    Raises:
    - Exits the program with a message if the response status code from HN is not 200.

    """
    URL = "https://news.ycombinator.com/news"
    response = requests.get(URL, params={"day": date})

    if response.status_code != 200:
        print("Failed to fetch the webpage.")
        exit()

    stories = []

    soup = BeautifulSoup(response.content, "html.parser")

    title_lines = soup.find_all("span", class_="titleline")
    sub_lines = soup.find_all("span", class_="subline")

    for rank, (title_line, sub_line) in enumerate(zip(title_lines, sub_lines), 1):
        title_tag = title_line.find("a")
        title = title_tag.text
        try:
            site = title_line.find("span", class_="sitestr").text
        except AttributeError:
            site = "news.ycombinator.com"
        if not link.startswith("http"):
            link = "https://news.ycombinator.com/" + link
        score = int(sub_line.find("span", class_="score").text.replace(" points", ""))
        author = sub_line.find("a", class_="hnuser").text
        try:
            comments_number = int(
                sub_line.find_all("a")[-1].text.replace("\xa0comments", "")
            )
        except ValueError:
            comments_number = 0

        story = {
            "rank": rank,
            "title": title,
            "site": site,
            "link": link,
            "score": score,
            "author": author,
            "comments_number": comments_number,
        }
        stories.append(story)

    stories_df = pd.DataFrame(stories)
    return stories_df
