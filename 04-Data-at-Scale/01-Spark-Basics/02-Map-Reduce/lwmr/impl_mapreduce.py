import time
from typing import Dict, List, Tuple
from multiprocessing import Pool, cpu_count

from lwmr.text_processing import get_words


NUM_JOBS = cpu_count()


def split_file_into_chunks(txt_path: str, n_chunk: int) -> List[str]:
    """
    Reads a large txt file and create and store many smallest files depending on the number of chunks
    Return the list of paths at which all each files are stored
    """

    pass  # YOUR CODE HERE


def simple_map_txt_file_to_word_and_one(txt_path) -> List[Tuple[str, int]]:
    """
    From a text file path, read its content and map each word to a tuple (word ,1)
    Returns: e.g: [(Car, 1),(Car, 1),(River,1), ...]
    """
    pass  # YOUR CODE HERE


def map_on_each_chunk(chunk_paths: List[str]) -> List[List[Tuple[str, int]]]:
    """Returns: A list of many lists
    e.g [
        (Car, 1),(Car, 1),(River,1), ...]
        (Dear, 1),(Bear, 1),(River,1), ...]
    """

    mapped_chunks = [
        simple_map_txt_file_to_word_and_one(chunk_path) for chunk_path in chunk_paths
    ]

    return mapped_chunks


def shuffle(
    word_groups_with_counts: List[List[Tuple[str, int]]]
) -> List[Tuple[str, List[int]]]:
    """
    Shuffle aggregates word counts for each group into a list of tuples containing the word and a list of the counts.

    For instance it takes as input:
    [
        [("Car", 1), ("Car", 1)],
        [("Dear", 1)],
    ]

    To return:
    [
        ("Car", [1, 1]),
        ("Dear", [1]),
    ]
    """
    pass  # YOUR CODE HERE





def final_reduce(shuffled_words: List[Tuple[str, List[int]]]) -> Dict[str, int]:
    """
    take a list of words with their list of ones and reduce it to a dict of words with their count within the text
    e.g: Input :
        [
            ("Car", [1, 1]),
            ("Dear", [1]),
        ]
    Output: {'Car': 2, 'Dear': 1}
    """

    pass  # YOUR CODE HERE


def count_words_mapreduce(txt_path_files: List[str]):
    mapped_chunks = map_on_each_chunk(txt_path_files)
    shuffled_words = shuffle(mapped_chunks)
    reduced = final_reduce(shuffled_words)

    return reduced


def count_words_mapreduce_multiproc(chunk_file_paths: List[str]):
    pass  # YOUR CODE HERE


if __name__ == "__main__":
    N_SPLIT = 64
    txt_file = "data/The_Data_Engineering_Cookbook.txt"
    txt_files = split_file_into_chunks(txt_file, N_SPLIT)

    print("👉Starting map-reduce single processing...")
    start = time.perf_counter()
    pass  # YOUR CODE HERE
    end = time.perf_counter()
