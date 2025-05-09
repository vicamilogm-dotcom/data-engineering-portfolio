import os
import sys
import random
import numpy as np
import datetime
import time
from google.cloud import pubsub_v1


def get_message_data(
    sensor_name: str, sensor_center_line: float, sensor_standard_deviation: float
) -> str:
    """generate messages for one specific sensor, with some variation around center value, with a random latency on the timestamp"""
    reading = np.random.normal(loc=sensor_center_line, scale=sensor_standard_deviation)
    latency = abs(random.gauss(0, 0.2))
    time.sleep(latency)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

    message = sensor_name + "," + str(reading) + "," + timestamp

    return message


def run(topic_name: str, project_id: str):
    """
    Simulates sensor data and publishes it to a messaging topic in a cloud service.

    This function simulates sensor readings from four different sensors with some
    variation and random latency. Each sensor generates a reading based on a normal
    distribution around a center value and publishes the data to the specified topic.

    Args:
        topic_name (str): The name of the topic to which the messages will be published.
        project_id (str): The ID of the project associated with the topic.

    The function runs indefinitely, continuously publishing messages to the topic until inturrupted.
    Every 100 messages, a status update is printed.
    """
    sensor_names = ["AtmP", "Temp", "Airtight", "H2OC"]
    sensor_center_lines = [989.21, 9.45, 1216.02, 9.64]
    standard_deviations = [8.35, 8.42, 39.98, 4.23]

    # Instanciate a PublisherClient Class from pubsub_v1
    publisher = None
    publisher = pubsub_v1.PublisherClient()

    # Construct the subscription path using the method `topic_path` of publisher
    topic_path = None
    topic_path = publisher.topic_path(project_id, topic_name)
    print(f"Publishing messages in {topic_path}..\n")

    c = 0
    while True:
        for i in range(len(sensor_names)):
            message = get_message_data(
                sensor_names[i], sensor_center_lines[i], standard_deviations[i]
            )

            # Publish message in topic using `publish` method
            # Carefull messages must be sent as a bytestring (encoded in 'utf-8')
            job = publisher.publish(topic_path, data=message.encode("utf-8"))

            job.result()

            c += 1

        if c == 100:
            print("Published 100 Messages")
            c = 0


if __name__ == "__main__":
    project_id = os.environ["PROJECT_ID"]
    topic_name = os.environ["TOPIC_NAME"]

    try:
        run(topic_name, project_id)
    except KeyboardInterrupt:
        print("Interrupted : Stopped Publishing messages")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
