
# Make sure to add the correct imports here
from typing import Optional, Union, List


def get_pokemon(limit: int = 100, offset: int = 0) -> dict:
    """Get a list of pokemon. Return a dictionary containing the results. Limit the results to `limit` and offset by `offset`"""
    pass  # YOUR CODE HERE


def check_pokemon_move(name: str = "bulbasaur", move: str = "swords-dance") -> bool:
    """Check if a pokemon can learn a move. Return True if it can, False otherwise."""
    pass  # YOUR CODE HERE


def get_pokemon_types(
    type_one: str = "flying", type_two: Optional[str] = None
) -> List[Optional[str]]:
    """
    Get all pokemon of a given type `type_one`. Return a list of pokemon names.
    If `type_two` is given return only the Pokemon of type_one and type_two.
    """
    pass  # YOUR CODE HERE


def get_evolutions(name: str) -> dict:
    """
    For a given pokemon return a dictionary containing the pokemon it evolves
    from and into. The structure should be:
    {"from": "pokemon_name", "to": ["pokemon_name"]}
    If the pokemon does not evolve from or into another pokemon
    do not include the relevant key.
    """
    pass  # YOUR CODE HERE
