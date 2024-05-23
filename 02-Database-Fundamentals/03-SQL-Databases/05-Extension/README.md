## Vector postgres

A vector database primarily stores vector representations of data, which are arrays of numbers, often in high-dimensional spaces. Here's a brief on their purposes:

1. **Similarity Search**: Enable similarity search operations, like nearest neighbor searches, which are essential in recommendation systems, image and video recognition, and other AI/ML applications.
2. **Dimensionality Reduction**: Handle dimensionality reduction efficiently, aiding in managing and processing high-dimensional data.
3. **Indexing**: Efficient indexing of high-dimensional data to speed up query processing.
4. **Distance Metrics**: Employ various distance metrics for similarity measurement, aiding in more accurate retrieval of data.
5. **Scalability**: Handle large-scale datasets and high query volumes, making them suitable for big data applications.

These databases are crucial in domains like computer vision, natural language processing, and other fields where vectorized representations of data are common.

Here we want to explore the use of vector databases in the context of postgres, we will use pgvector.

🎯 Use pgvector to create a system to find similar reviews

Here is an interesting article on what a word vector is https://dzone.com/articles/introduction-to-word-vectors

### Installation

Create a new database called `test-vector`

Install postgres 14 dev tools

```bash
sudo apt install postgresql-server-dev-14
```

Install pgvector from source

```bash
cd /tmp
git clone --branch v0.5.1 https://github.com/pgvector/pgvector.git
cd pgvector
make
make install
```

Connect to the database and create the extension

```bash
CREATE EXTENSION vector;
```

### Usage


Download this data

https://www.kaggle.com/datasets/jrobischon/wikipedia-movie-plots

put it in the `data` folder

### Create the table

Use `create_table.py` all you need to is finish the main to create a connection and make the table!

### Insert the data

❓ Implement `upload_data.py`

There is a function in `vectorize` to convert a string to 128 dimensional vector you need to read the data and use this on each plot to add plot_vector to the dataframe read in. Then upload to the table you already created.

### Query the data

Implement `nearest_movies.py` and test it out with some different descriptions!

Checkout these docs if you get stuck https://github.com/pgvector/pgvector-python
