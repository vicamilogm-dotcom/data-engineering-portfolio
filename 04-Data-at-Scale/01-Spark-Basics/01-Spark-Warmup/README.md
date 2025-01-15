# 🎯 Goal

This exercise is meant to be some practice for learning **PySpark** syntax. The rest of the unit will mostly explore other scaling up techniques. The next unit will involve a more in depth exercise with PySpark. Building an entire end to end pipeline!

<br>

# 1️⃣ Data

For this challenge we will use an [e-commerce dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) from Kaggle for the questions in this challenge:

Download with the following command:

```bash
kaggle datasets download -d olistbr/brazilian-ecommerce --unzip -p ./data
```

We want the CSV files to end up in the directory: `00-Spark-warmup/data/`

Make sure to familiarise yourself with the different tables and fields. We recommend keeping the kaggle page open for a quick reference!

<br>

# 2️⃣ Spark warmup

Open up `exercise.ipynb`, make sure that your Poetry environment is selected in the jupyter notebook - top right corner, select kernel - and get started solving the exercise!

There are tests inside the jupyter notebook. Don't worry about the notes in the tests telling you to push `master`.

🧪 Once you've completed the notebook, test with:

```bash
make test
```

And don't forget to git add, commit, and push your code to Github to track your progress on Kitt.

<br>
