# 🎯 Goal

Pandas is crucial for data engineering because it simplifies data manipulation, integration, exploration, and analysis. It offers powerful tools, like **DataFrames** and **vectorized operations**, which enable effortless cleaning, transforming, and reshaping of data. 🧹💪

Pandas seamlessly integrates multiple data sources and supports various file formats, facilitating data integration. 📂🔄

Handling missing data is made easier with pandas' methods for filling, dropping, or interpolating values. 📊🔍

The library provides statistical analysis, descriptive statistics, and data visualization functions for data exploration. 📈📉

By leveraging efficient data structures and operations, pandas improves computational speed and memory utilization. ⚡💾

Once data processing is complete, pandas allows for easy data export or integration with other tools or libraries. 📤🔧

Overall, pandas serves as a versatile tool for data engineers, boosting productivity and efficiency in their work.

<br>

# 0️⃣ Data

We are going to be using Kaggle, an online community and platform for data scientists and machine learning practitioners that offers datasets, competitions, notebooks, and learning resources. Most importantly **lots of great datasets are shared here!**

Install the kaggle cli 👇

```bash
# globally with pipx - available from anywhere!
pipx install kaggle
```

Then follow the [instructions](https://github.com/Kaggle/kaggle-api/blob/main/docs/README.md#api-credentials) in the API credentials section to allow the cli to work!

We'll use this tabular [Goodreads dataset](https://www.kaggle.com/datasets/mohamedbakhet/amazon-books-reviews) for this challenge.

Once you have done this **run the following command to download the dataset**:

```bash
kaggle datasets download -d mohamedbakhet/amazon-books-reviews --unzip -p ./data
```

<br>

# 1️⃣ Pandas pipeline

We want to use pandas to build a data pipeline. We have two CSV files at the moment: `books_data.csv` and `Books_rating.csv`. The pipeline specifications are written out below. After completing Step 1 you can work in any order, more specific instructions are included in all of the functions docstring's!

1. Complete `pandas_pipeline/load.py` which loads data relevant data from an input path.
2. Complete `pandas_pipeline/best_books.py` which will generate a CSV file of the top 10 best performing books based on their average review score.
🧪 Test
```bash
pytest -k test_best_performing_books_csv
```
3. Complete `pandas_pipeline/category_distribution.py` which will generate a CSV file of the book categories distribution.
🧪 Test
```bash
pytest -k test_category_distribution_csv
```
4. Complete `pandas_pipeline/top_authors.py` which will generate a CSV of the 10 most impactful authors based on their average score and number of reviews.
🧪 Test
```bash
pytest -k test_author_impact_analysis_csv
```
5. Complete `pandas_pipeline/review_years.py` that will calculate the average review scores over time and save the results to a CSV file
🧪 Test
```bash
pytest -k test_review_years_csv
```

<br>

# 🏁 Finish

Once each of the functions work run the entire pipeline with:

```bash
python pandas_pipeline/pipeline.py
```

And have a look at the output!

🧪 Test all of your code with:

```bash
make test
```

And don't forget to commit and push all your code to github 🚀

<br>
