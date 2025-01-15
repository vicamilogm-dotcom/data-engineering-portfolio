from vector_movies.create_table import Movie
from vector_movies.vectorize import create_vectorized_representation
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from typing import List, Tuple

# Define your engine and session
pass  # YOUR CODE HERE


def get_nearest_movies(description: str, n=5) -> List[Tuple[str, str]]:
    """
    Retrieves a list of movies that have the most similar plot descriptions to the given description.

    Parameters:
    description (str): The movie description used for similarity comparison.
    n (int, optional): The number of similar movies to retrieve. Defaults to 5.

    Returns:
    List[Tuple[str, str]]: A list of tuples where each tuple contains the title and plot description of a similar movie.
    """
    pass  # YOUR CODE HERE


if __name__ == "__main__":
    print(get_nearest_movies("Great freinds go on a road trip.", 2))
