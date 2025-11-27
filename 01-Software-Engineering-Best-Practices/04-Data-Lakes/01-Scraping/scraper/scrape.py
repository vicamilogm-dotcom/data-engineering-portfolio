import sys
from typing import List, Dict

import requests
import pandas as pd
from bs4 import BeautifulSoup

BASE_URL = "https://news.ycombinator.com/front?day={date}"


def scrape_hn(date: str) -> pd.DataFrame:
    """
    Scrape Hacker News front page for a given date.

    Parameters
    ----------
    date : str
        Date in format YYYY-MM-DD.

    Returns
    -------
    pd.DataFrame
        DataFrame with one row per story and the columns:
        - rank (int)
        - title (str)
        - site (str or None)
        - link (str)
        - score (int)
        - author (str or None)
        - comments_number (int)
    """
    url = BASE_URL.format(date=date)

    # 1. Petición HTTP con manejo de errores
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as exc:
        print(f"Error while requesting {url}: {exc}")
        sys.exit(1)

    # 2. Parseo del HTML
    soup = BeautifulSoup(response.text, "html.parser")

    stories: List[Dict] = []

    # Cada historia está en una fila <tr class="athing">
    for rank, row in enumerate(soup.select("tr.athing"), start=1):
        # Título y link principal
        title_tag = row.select_one("span.titleline a")
        if title_tag is None:
            continue

        title = title_tag.get_text(strip=True)
        link = title_tag.get("href", "")

        # Sitio (dominio), si está disponible
        site = None
        site_tag = row.select_one("span.sitestr")
        if site_tag is not None:
            site = site_tag.get_text(strip=True)

        # Valores por defecto
        score = 0
        author = None
        comments_number = 0

        # Fila siguiente: subtexto (puntuación, autor, comentarios, etc.)
        next_row = row.find_next_sibling("tr")
        subtext_td = next_row.select_one("td.subtext") if next_row is not None else None

        if subtext_td is not None:
            # Score: span.score → "123 points"
            score_tag = subtext_td.select_one("span.score")
            if score_tag is not None:
                score_text = score_tag.get_text(strip=True)
                try:
                    # Nos quedamos con el número inicial
                    score = int(score_text.split()[0])
                except (ValueError, IndexError):
                    score = 0

            # Autor
            author_tag = subtext_td.select_one("a.hnuser")
            if author_tag is not None:
                author = author_tag.get_text(strip=True)

            # Número de comentarios: último enlace suele ser "NN comments"
            links = subtext_td.find_all("a")
            if links:
                comments_text = links[-1].get_text(strip=True)
                if "comment" in comments_text:
                    try:
                        comments_number = int(comments_text.split()[0])
                    except (ValueError, IndexError):
                        comments_number = 0

        stories.append(
            {
                "rank": rank,
                "title": title,
                "site": site,
                "link": link,
                "score": score,
                "author": author,
                "comments_number": comments_number,
            }
        )

    return pd.DataFrame(stories)
