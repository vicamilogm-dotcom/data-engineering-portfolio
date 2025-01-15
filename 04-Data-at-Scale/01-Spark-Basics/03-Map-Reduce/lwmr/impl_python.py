from typing import Dict
import time

from lwmr.text_processing import get_words


def count_words(txt: str) -> Dict[str, int]:
    """
    Given a text input, returns a dictionary for each word and its number of occurrences.

    Example: count_words("I love apples, bananas and apples") would return
    {
        "I": 1,
        "love": 1,
        "apples": 2,
        "bananas": 1,
        "and": 1
    }
    """

    pass  # YOUR CODE HERE


if __name__ == "__main__":
    txt_path = "data/The_Data_Engineering_Cookbook.txt"

    with open(txt_path, "r") as f:
        txt = f.read()

    print("👉Starting single processing...")
    start = time.perf_counter()
    l_counts = count_words(txt)
    end = time.perf_counter()
    print(f"✅ Done in {end-start} seconds \n")
