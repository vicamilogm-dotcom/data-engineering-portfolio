import time
from typing import Dict, List, Tuple
from multiprocessing import Pool, cpu_count
from lwmr.text_processing import get_words

NUM_JOBS = cpu_count()  # Número de procesos (nucleos del CPU)

def split_file_into_chunks(txt_path: str, n_chunk: int) -> List[str]:
    """
    Divide el archivo en n_chunk partes.
    Devuelve una lista de las rutas a cada uno de los archivos creados.
    """
    chunk_paths = []
    with open(txt_path, "r") as f:
        lines = f.readlines()

    # Calculamos cuántas líneas por archivo
    chunk_size = len(lines) // n_chunk
    for i in range(n_chunk):
        chunk_file = f"{txt_path}_chunk_{i}.txt"
        start = i * chunk_size
        end = (i + 1) * chunk_size if i < n_chunk - 1 else len(lines)
        with open(chunk_file, "w") as chunk_f:
            chunk_f.writelines(lines[start:end])
        chunk_paths.append(chunk_file)

    return chunk_paths


def simple_map_txt_file_to_word_and_one(txt_path: str) -> List[Tuple[str, int]]:
    """
    Lee el contenido de un archivo de texto y mapea cada palabra a una tupla (palabra, 1)
    Devuelve una lista de tuplas.
    """
    word_count = []
    with open(txt_path, "r") as f:
        words = get_words(f.read())  # Usamos get_words para extraer las palabras

    # Asignamos la tupla (palabra, 1) para cada palabra
    word_count = [(word, 1) for word in words]

    return word_count


def map_on_each_chunk(chunk_paths: List[str]) -> List[List[Tuple[str, int]]]:
    """
    Aplica el mapeo a cada trozo de archivo.
    Devuelve una lista de listas de tuplas.
    """
    mapped_chunks = [simple_map_txt_file_to_word_and_one(chunk_path) for chunk_path in chunk_paths]
    return mapped_chunks


def shuffle(word_groups_with_counts: List[List[Tuple[str, int]]]) -> List[Tuple[str, List[int]]]:
    """
    Agrupa las palabras con sus contadores y devuelve una lista de tuplas.
    """
    shuffled = {}
    for group in word_groups_with_counts:
        for word, count in group:
            if word not in shuffled:
                shuffled[word] = []
            shuffled[word].append(count)

    # Convertimos el diccionario en una lista de tuplas
    return list(shuffled.items())


def final_reduce(shuffled_words: List[Tuple[str, List[int]]]) -> Dict[str, int]:
    """
    Suma los valores de las listas de contadores y devuelve un diccionario final de palabras con su conteo.
    """
    reduced = {word: sum(counts) for word, counts in shuffled_words}
    return reduced


def count_words_mapreduce(txt_path_files: List[str]) -> Dict[str, int]:
    """
    Implementa el proceso completo de Map-Reduce para contar palabras.
    """
    mapped_chunks = map_on_each_chunk(txt_path_files)
    shuffled_words = shuffle(mapped_chunks)
    reduced = final_reduce(shuffled_words)
    return reduced


def count_words_mapreduce_multiproc(chunk_file_paths: List[str]) -> Dict[str, int]:
    """
    Implementa Map-Reduce utilizando multiprocesamiento para paralelizar el trabajo.
    """
    # Dividimos el trabajo en procesos
    with Pool(processes=NUM_JOBS) as pool:
        result = pool.map(simple_map_txt_file_to_word_and_one, chunk_file_paths)

    # Hacemos el shuffle y reduce
    shuffled_words = shuffle(result)
    reduced = final_reduce(shuffled_words)

    return reduced


if __name__ == "__main__":
    N_SPLIT = 64
    txt_file = "data/The_Data_Engineering_Cookbook.txt"

    # Dividimos el archivo en 64 partes
    txt_files = split_file_into_chunks(txt_file, N_SPLIT)

    # Realizamos el procesamiento Map-Reduce
    print("👉Starting map-reduce single processing...")
    start = time.perf_counter()
    word_counts = count_words_mapreduce(txt_files)
    end = time.perf_counter()
    print(f"✅ Done in {end - start} seconds")
    print(f"Most frequent words: {dict(list(word_counts.items())[:10])}")

    # Realizamos el procesamiento Map-Reduce con multiprocesamiento
    print("👉Starting map-reduce multiproc processing...")
    start = time.perf_counter()
    word_counts_multiproc = count_words_mapreduce_multiproc(txt_files)
    end = time.perf_counter()
    print(f"✅ Done in {end - start} seconds")
    print(f"Most frequent words (multiproc): {dict(list(word_counts_multiproc.items())[:10])}")