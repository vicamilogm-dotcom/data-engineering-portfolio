<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W3D3-processing/pyspark/pyspark.jpeg" alt="drawing" width="400"/>

### 1️⃣ Set-up
Go to https://www.databricks.com/try-databricks and set up an account.
Don't choose a cloud provider, just use the free `Community Edition` (well hidden)

<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W3D3-processing/databrick-login.png">

Databricks is a company that provides a cloud platform, allowing you to easily set up a PySpark cluster for free.

Once you have create an account. Go to the `compute` folder in Databricks and click on `Create compute` in order to create a cluster. Pick a name and choose the default settings. You will create an instance with 15gb of memory and 2 Cores, allowing you to do some minimal parallel processing 😀. While this cluster is being created, have a look at the Polars notebook 👇

### 2️⃣  Polars
❓ In the polars subdirectory you can find a jupyter notebook file that contains a comparison of Pandas and `Polars`. Contrary to Pandas, Polars uses multiple CPU cores on your machine, which allows for parallel processing. It has other features as well, like lazy evaluation and query optimization. Go through the notebook to learn more about this. Really try to understand these different features and read more about them if they are not clear yet.

### 3️⃣ Pyspark
Polars is able to process data that is larger than what fits in memory. However, this is a very new library and not something that we have often come across in production settings. What is very common though in a production environment is `PySpark`.

Where `Polars` is able to run huge datasets on a single machine, `PySpark` makes it possible to run transformations on multiple machines. Just like `Polars`, `PySpark` uses lazy evaluation to only return any results once the data is so-called "collected". It also optimizes the query to improve performance.

❓ Download the `pyspark/pyspark.ipynb` as a file

<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W3D3-processing/pyspark/download_file.png" alt="drawing" width="600"/>

❓ Import it into Databricks Community.

<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W3D3-processing/pyspark/import-notebook.png" alt="drawing" width="600"/>

❓ Follow the instructions in that notebook.
