import os
import psycopg2


def get_env_vars():
    """
    Retrieve PostgreSQL user and password from environment variables.

    Returns
    -------
    str, str
        PostgreSQL username and password.
    """
    pass  # YOUR CODE HERE


def get_words():
    """
    Prompt user for words to search for.

    Returns
    -------
    str
        The combined search words as a tsquery-compatible string.
    """
    pass  # YOUR CODE HERE


def execute_query(cur, words_str):
    """
    Execute a text search query and return results, ordered by ranking.

    Parameters
    ----------
    cur : psycopg2.extensions.cursor
        Database cursor.
    words_str : str
        Search query string.

    Returns
    -------
    list of tuple
        List of movie titles and their corresponding ranks.
    """
    pass  # YOUR CODE HERE


def main():
    """
    Main function to perform text search on a PostgreSQL database.
    """
    pass  # YOUR CODE HERE


if __name__ == "__main__":
    main()
