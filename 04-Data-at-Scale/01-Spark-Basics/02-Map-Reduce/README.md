# 🎯 Context and Goals

In the world of big data processing, the [divide and conquer](https://en.wikipedia.org/wiki/Divide-and-conquer_algorithm) strategy is a must-know.

It works as follows:

- Datasets are split into smaller datasets ✂️.
- An intermediate algorithm is applied to each smaller dataset ⛏️.
- The results on each intermediate, smaller dataset are aggregated to make the final result 🔗.

The equivalent of the ["Hello, World!"](https://en.wikipedia.org/wiki/%22Hello,_World!%22_program) program for big data processing is the **word count problem**:

**Problem: we have a large book, and would like to compute the number of occurrences of each word**

Big data technology has evolved over the years. The APIs have gotten more developer friendly and powerful over the years. In this exercise, we'll implement several versions of the same algorithm, with a jump in history every time 📜.

For the book, we'll use [The Data Engineering Cookbook](https://www.darwinpricing.com/training/Data_Engineering_Cookbook.pdf) by [Andreas Kretz](https://www.linkedin.com/in/andreas-kretz/?originalSubdomain=de), CEO of [LearnDataEngineering.com](https://learndataengineering.com/).

We've extracted the text into a [text file you can download](https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W3D3-processing/The_Data_Engineering_Cookbook.txt)
and duplicated the text many times (just to make the computation heavy 😅). You can store it under `data/The_Data_Engineering_Cookbook.txt`

<br>

# 1️⃣ Basic Python Word Counter

❓ Setup: Run `poetry install` to be sure your packages are up to date.

❓ Let's implement a very basic counter in Python in `impl_python.py`. We will use it as a baseline against the other methods we'll implement later.

🧪 Once you think you're done with the basic counter, test with:

```bash
make test
```

The first two tests should pass.

<br>

# 2️⃣ Implement Map-Reduce purely in Python

## 2.1. The big picture

As its name indicates, the Map-Reduce paradigm follows steps of mapping then (optionally, but usually) reducing.

We'll implement the algorithim in Python with the following steps, described on the following flowchart:

<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/map-flowchart.png" width=600>

👉 In the `lwmr/impl_mapreduce.py` file, you will see one function for each of the steps. The function signatures and description indicate what the input looks like and what the output should be.

<br>

**The code flow is presented below**

```python
N_CHUNK = 64 # Suggested split number to use for the cookbook dataset
txt_path = "data/The_Data_Engineering_Cookbook.txt"

# 0. SPLITTING
txt_files_paths = split_file_into_chunks(txt_path, n_chunk)
# --> Returns 64 paths to 64 small text files saved to disk, simulate HDFS chunks in separate nodes

# 1. MAPPING
mapped_chunks = map_on_each_chunk(txt_path_files)
# --> 64 lists of lists like [(Car, 1),(Car, 1),(River,1), ...]

# 2. SHUFFLING
shuffled_words = shuffle(mapped_chunks)
# --> 1 big list of tuples: e.g [('Car', [1, 1]), ('River', [1]), ...]

# 3. REDUCING
reduced = final_reduce(shuffled_words)
## --> 1 big dict of words: e.g. {'Car': 2, 'River': 1}
```

While word count is the most typical example to showcase Map/Reduce, its breakdown can feel a bit convoluted. If it doesn't feel intuitive, that's normal!

The key concept to understand in Map/Reduce is: we are looking for opportunities to parallelize our work. This means whenever possible, we will apply transformations that allow us to have multiple servers run computation in parallel (`map` steps). Once the computation on all servers are done, the results of the mapping step are coordinated and aggregated in a `reduce` phase.

## 2.2. Implementation

### Splitting - implementing `split_file_into_chunks`

💡 For debugging purposes, we advise you to start with creating a very small text file made of only with few sentences, and `N_CHUNK=2`. It will make it faster and smaller to print & debug.

### Mapping - Implement `map_on_each_chunk`

The function `map_on_each_chunk` takes a list of paths to each chunk.

⏩ In production this would be done in parallel and provide a huge performance benefit!

### Shuffling - Implement `shuffle`

The shuffle function aggregates word counts for each group by word.

### Reducing - Implement `final_reduce`

The reduce function is a simple sum of all "ones" for each word that is going to give the final **counts for each word** 🎉

<br>

# 3️⃣ Putting everything together

The goal is to first put your map reduce together as a single process, then implement a multi-process version!

## 3.1. Single processing

**Implement the `count_words_mapreduce` function**

Here as inputs we have:

- Inputs: the list of paths of chunks

The ouput is ultimately the count of words going through the 3 steps: Map/Shuffle/Reduce


## 3.2. Multiprocessing

**Implement the `count_words_mapreduce_multiproc` function**

There is a few things to consider:
- You'll have to instantiate a pool of workers and map each single function
- You'll have to think about how to parallelize the work.
- Not all steps are possible to parallelize
- Most of the blocks of code are already available, but refactor if you see some code used more than once!


<details>
  <summary markdown='span'>💡 Hint</summary>

  The `shuffle` function part needs to gather all the words together and it cannot easily run in parallel processes.

</details>

## 3.3. Compare both implementations

You can time the execution of all implementations. Make sure to open `htop` in a new terminal to see the parallel processes using all of your CPU cores.

<br>

# 🏁 Finish

We've demonstrated the power of parallized operations and Map-Reduce.

🧪 Once you have finished comparing the run times of both implementations, test all of your code with:

```bash
make test
```

And don't forget to git add, commit and push your code to github so Kitt can track your progress 🚀

<br>
