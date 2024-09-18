from PIL import Image
import numpy as np
import pathlib
import random
import tensorflow as tf

DATA_PATH = pathlib.Path(__file__).resolve().parent.parent / "data" / "chest_xray"
random.seed(42)


def get_image_paths() -> list:
    """
    Returns a list of all image paths in the data directory inside tuples of the form (label, path) with
    1 for PNEUMONIA and 0 for NORMAL. Make sure that the list is shuffled
    """
    pass  # YOUR CODE HERE


def process_image(path: str) -> np.ndarray:
    """
    Returns a numpy array of shape (256, 256, 1) with the image data from the given path
    """
    pass  # YOUR CODE HERE


def write_image(writer, image, label):
    """
    Writes the given image and label to the given writer
    """
    feature = {
        "image": tf.train.Feature(
            bytes_list=tf.train.BytesList(value=[image.tobytes()])
        ),
        "label": tf.train.Feature(int64_list=tf.train.Int64List(value=[label])),
    }
    pass  # YOUR CODE HERE


def main():
    writer = tf.io.TFRecordWriter("dataset.tfrecords")
    for label, path in get_image_paths():
        image = process_image(path)
        write_image(writer, image, label)


if __name__ == "__main__":
    print(get_image_paths())
