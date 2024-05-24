# 🎯 Goals and Introduction

The goal of this exercise is to process and write image data to a TFRecord file using TensorFlow and PIL libraries. This is an example of preparing data for a data science team rather than analytics as the format is optimal for training machine learning models!

We will be using a dataset of chest X-ray images to create a TFRecord file. The dataset contains images of two classes: NORMAL and PNEUMONIA. We will begin with some basic image processing tasks and then move into writing the processed images to a TFRecord file.

- Check the documentation and understand how to use PIL and TensorFlow libraries for image processing and writing to a TFRecord file.

- Make sure you **understand how to manipulate image data using numpy arrays.**

- Test your functions thoroughly to ensure they are working as expected.

<br>

# 0️⃣ Getting the data

We are going to be using Kaggle, an online community and platform for data scientists and machine learning practitioners that offers datasets, competitions, notebooks, and learning resources. Most importantly **lots of great datasets are shared here!**

Install the kaggle cli 👇
```bash
pipx install kaggle
```

Then follow the [instructions](https://github.com/Kaggle/kaggle-api) in the API credentials section to allow the cli to work!

Once you have done this **run this command  to download the dataset!**
```bash
kaggle datasets download -d paultimothymooney/chest-xray-pneumonia --unzip -p ./data
```

<br>

# 1️⃣ Get image paths

In the `process.py` file, your first task is to complete the function `get_image_paths`. This function is expected to return a list of all image paths in the data directory. Each item in the list should be a tuple of the form (label, path), where the label is 1 for PNEUMONIA and 0 for NORMAL. Additionally, the list should be shuffled to ensure randomness.

```python
def get_image_paths() -> list:
    """
    Returns a list of all image paths in the data directory inside tuples of the form (label, path) with
    1 for PNEUMONIA and 0 for NORMAL. Make sure that the list is shuffled
    """
    pass  # YOUR CODE HERE
```

Try and implement `get_image_paths`, test using the `__main__` block as you go if you like!


<details>
<summary markdown='span'>💡 Hints</summary>
Use the pathlib library to navigate the directory structure and glob to find all the relevant image files. Remember to shuffle the final list before returning it.


</details>

🧪 Once you think your function works you can test it with this command:

```bash
pytest tests/test_process.py::TestImageProcessing::test_get_image_paths
```

<br>

# 2️⃣ Process image

The next function you need to complete is `process_image`. This function should take a path to an image as input and return a numpy array of shape (256, 256, 1) containing the processed image data.

```python
def process_image(path: str) -> np.ndarray:
    """
    Returns a numpy array of shape (256, 256, 1) with the image data from the given path
    """
    pass  # YOUR CODE HERE
```

❓ Use the PIL library to open and resize the image. Then, convert the image to a numpy array and normalize the pixel values to the range [0, 1].

🧪 Test your function with this command:

```bash
pytest tests/test_process.py::TestImageProcessing::test_process_image
```

<br>

# 3️⃣ Write image

The final function you need to complete is `write_image`. This function should take a writer, an image, and a label as input and write the image and label to the writer in the TFRecord format.

```python
def write_image(writer, image, label):
    """
    Writes the given image and label to the given writer
    """
    pass  # YOUR CODE HERE
```

❓ Use the TensorFlow library to create a tf.train.Example object containing the image and label data. Then, serialize the example object and write it to the writer.

🧪 Test your function with this command:

```bash
pytest tests/test_process.py::TestImageProcessing::test_write_image
```

<br>

# 🏁 Final Steps

🧪 Once you have completed all the functions and passed all the tests, it's time to run all the tests together:

```bash
make test
```

If all tests pass, congratulations! 🚀 You have successfully completed this exercise. Commit your changes and push your code to github:

```bash
git add --all
git commit -m "finished image processing exercise"
git push origin main
```

<br>
