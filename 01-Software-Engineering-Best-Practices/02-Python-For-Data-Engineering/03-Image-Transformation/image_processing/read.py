import tensorflow as tf


def parse_example(example):
    feature_description = {
        "image": tf.io.FixedLenFeature([], tf.string),
        "label": tf.io.FixedLenFeature([], tf.int64),
    }
    parsed_example = tf.io.parse_single_example(example, feature_description)

    image = tf.io.decode_raw(parsed_example["image"], out_type=tf.float64)
    image = tf.reshape(image, [256, 256, 1])

    label = parsed_example["label"]

    return image, label


if __name__ == "__main__":
    dataset = tf.data.TFRecordDataset("dataset.tfrecords")

    dataset = dataset.map(parse_example)

    for image, label in dataset:
        print(image)
        print(label)
