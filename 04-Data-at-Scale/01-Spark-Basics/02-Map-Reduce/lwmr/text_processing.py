from typing import List
import string
import re


def get_words(txt: str) -> List[str]:
    """
    Extracts words from text
    """
    for punc in list(string.punctuation) + ["[", "(", ")", "]", "`"]:
        txt = txt.replace(punc, "")

    return [x.lower() for x in re.split("[\s+]", txt) if len(x) > 0]


if __name__ == "__main__":
    with open("data/The_Data_Engineering_Cookbook.txt", mode="r") as f:
        txt = f.read()
        words = get_words(txt)
        print(words[0:10])
