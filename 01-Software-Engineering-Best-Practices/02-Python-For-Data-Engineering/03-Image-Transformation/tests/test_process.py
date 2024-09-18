import os
import tensorflow as tf
import numpy as np
from PIL import Image
import pathlib
import tempfile
import unittest
from unittest.mock import patch, MagicMock
from image_processing.process import get_image_paths, process_image, write_image


class TestImageProcessing(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_dir = tempfile.TemporaryDirectory()
        for i in range(5):
            img = Image.new(mode="L", size=(256, 256))
            img.save(cls.test_dir.name + f"/test_image_{i}.jpeg")

    @classmethod
    def tearDownClass(cls):
        cls.test_dir.cleanup()

    @patch("image_processing.process.DATA_PATH", new_callable=MagicMock)
    def test_get_image_paths(self, mock_data_path):
        mock_data_path.glob.side_effect = [
            [
                pathlib.Path(self.test_dir.name + f"/test_image_{i}.jpeg")
                for i in range(3)
            ],
            [
                pathlib.Path(self.test_dir.name + f"/test_image_{i}.jpeg")
                for i in range(3, 5)
            ],
        ]
        image_paths = get_image_paths()
        self.assertEqual(len(image_paths), 5)

    def test_process_image(self):
        for i in range(5):
            path = self.test_dir.name + f"/test_image_{i}.jpeg"
            processed = process_image(path)
            self.assertIsInstance(processed, np.ndarray)
            self.assertEqual(processed.shape, (256, 256, 1))

    def test_write_image(self):
        tfrecord_path = os.path.join(self.test_dir.name, "test.tfrecord")
        with tf.io.TFRecordWriter(tfrecord_path) as writer:
            for i in range(5):
                path = self.test_dir.name + f"/test_image_{i}.jpeg"
                processed = process_image(path)
                write_image(writer, processed, i % 2)

        raw_image_dataset = tf.data.TFRecordDataset(tfrecord_path)

        feature_description = {
            "image": tf.io.FixedLenFeature([], tf.string),
            "label": tf.io.FixedLenFeature([], tf.int64),
        }

        def _parse_image_function(example_proto):
            return tf.io.parse_single_example(example_proto, feature_description)

        parsed_image_dataset = raw_image_dataset.map(_parse_image_function)

        images = []
        labels = []
        for image_features in parsed_image_dataset:
            image_raw = image_features["image"].numpy()
            label = image_features["label"].numpy()
            image = np.frombuffer(image_raw, np.float64)
            image = image.reshape((256, 256, 1))
            images.append(image)
            labels.append(label)

        self.assertEqual(len(images), 5)
        self.assertEqual(len(labels), 5)

        for i in range(5):
            path = self.test_dir.name + f"/test_image_{i}.jpeg"
            expected_image = process_image(path)
            self.assertTrue(np.array_equal(images[i], expected_image))
            self.assertEqual(labels[i], i % 2)
