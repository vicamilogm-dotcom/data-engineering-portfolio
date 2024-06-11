# 🎯 Goals and Context

The goal for today is to setup a process which will:

1. Scrape stories from [hackernews](https://news.ycombinator.com/front)
2. Upload them to a data lake
3. Verify the quality of the data
4. Transform the data
5. Allow scoped access to the data

This first challenge will be about scraping the data from [hackernews](https://news.ycombinator.com/front). We will use a popular Python web scraping library, 🍜 [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/).

## Introduction to Web Scraping

Web scraping is the process of extracting data from websites. This involves making requests to websites and then parsing the returned HTML to extract the desired data.

## BeautifulSoup

🍜 [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) is a Python library widely used for web scraping. It parses HTML and XML documents and extracts data in a hierarchical and readable manner.

### Basic Example with BeautifulSoup

Consider the following scenario: You want to extract the title of a Wikipedia page. This is how you would execute that in code with BeautifulSoup!

```python
import requests
from bs4 import BeautifulSoup

URL = "https://en.wikipedia.org/wiki/Web_scraping"
response = requests.get(URL)
soup = BeautifulSoup(response.content, 'html.parser')
title = soup.title.text
print(title)  # Outputs: Web scraping - Wikipedia
```

With a bit of context and documentation to reference, let's build our webscraper!

<br>

# 1️⃣ Setting up the scraper function:

1. In the `scrape.py` file, initialize the `scrape_hn(date: str) -> pd.DataFrame` function.
2. Make a GET request to the [hackernews](https://news.ycombinator.com/front) website to retrieve the top stories for the given date.
3. Check the response status. If it's not 200 (HTTP OK), handle the error gracefully.

💡 **Hint**: Use the `requests` library for making HTTP requests. Have a look at the [documentation](https://requests.readthedocs.io/en/latest/user/quickstart/) for how to check the `Response Status Code`.

<br>

# 2️⃣ Parsing the HTML:

⏰ Warning: This can be quite a timely task especially if you are new to web scraping. Give it a go and if you stuck after 30 mins have a look at the solution at the bottom of this section if you need. If you do reference the solution, take a few minutes to read through the code and understand what is happening:

1. Use BeautifulSoup to parse the returned HTML.
2. Locate the relevant HTML elements containing story details, like titles, links, and author names.
3. Extract the data and store it in an appropriate data structure - a list of dictionaries.

💡 **Hint**: You can use the browser's developer tools to inspect the HTML structure of the Hacker News website. This will help you identify the tags and classes containing the desired information.


<details>
<summary markdown='span'>🎁 Solution</summary>

```python
    URL = "https://news.ycombinator.com/front"
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
            site = "https://news.ycombinator.com/"
        link = title_tag["href"]
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
```
</details>

<br>

# 3️⃣ Saving to CSV:

Scraping the data is awesome, but we are going to have to save it locally before uploading it to our data lake.

1. Convert the list of dictionaries into a pandas DataFrame.
2. In the `main.py` file, call the `scrape_hn` function to fetch the data for the current date.
3. Save the DataFrame to a CSV file named `stories.csv`.

💡 **Hint**: Pandas provides a convenient `to_csv` method to save DataFrames to CSV files. Remember to set `index=False` to avoid saving the DataFrame index to the CSV.

<br>

# 4️⃣ Error Handling:

We should be striving to create robust code that can deal with edge cases and fails gracefully.

1. Ensure your scraper handles exceptions gracefully, such as missing elements or network errors.
2. Consider adding retries or delays to respect the website's terms and prevent overloading it.

💡 **Hint**: The `try` and `except` blocks in Python can be used to catch and handle exceptions. It is best practice to always catch a specific exception (like `requests.exceptions.RequestException`) to handle known issues.

<br>

# 🏁 Finish

🧪 Once you are done with the challenge, test your code with:

```bash
make test
```

If the test passes, run `main.py` directly and have a look at the `csv` it creates to make sure it's working as intended!

Don't forget to push your code to github so Kitt can track your progress!

Now you are extracting `stories.csv` from [hackernews](https://news.ycombinator.com/front). You are ready to move on and begin uploading data to your lake!

<br>
