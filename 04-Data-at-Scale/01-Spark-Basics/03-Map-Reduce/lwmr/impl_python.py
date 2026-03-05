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
    words = get_words(txt)  # Usamos la función get_words para obtener todas las palabras

    word_count = {}
    for word in words:
        word_count[word] = word_count.get(word, 0) + 1  # Contamos las ocurrencias

    return word_count  # Devolvemos el diccionario con los resultados

if __name__ == "__main__":
    txt_path = "data/The_Data_Engineering_Cookbook.txt"

    with open(txt_path, "r") as f:
        txt = f.read()

    print("👉Starting single processing...")
    start = time.perf_counter()
    l_counts = count_words(txt)  # Llamamos a la función que cuenta las palabras
    end = time.perf_counter()
    
    # Mostramos un resumen de las primeras 10 palabras más frecuentes
    print(f"✅ Done in {end-start} seconds")
    print(f"Most frequent words: {dict(list(l_counts.items())[:10])}")