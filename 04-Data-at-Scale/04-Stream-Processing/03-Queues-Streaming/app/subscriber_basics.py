from google.cloud import pubsub_v1
import os
import sys


def callback(message: pubsub_v1.types.message):
    """
    Define the action to perform when receiving a message:
    print it and ack the received message.
    """
    pass  # YOUR CODE HERE


def run(subscription_name: str, project_id: str):
    """
    Starts a Pub/Sub subscriber client to listen for messages on a specified subscription.
    When a message is received, the provided `callback` function is triggered.

    Args:
        subscription_name (str): The name of the Pub/Sub subscription to listen to.
        project_id (str): The GCP project ID where the Pub/Sub subscription resides.

    The function runs indefinitely, waiting for messages until interrupted.
    """
    # 1. Instantiate a pubsub SubscriberClient Class named `subscriber`
    subscriber = None
    pass  # YOUR CODE HERE

    # 2. Construct the subscription path using the method `subscription_path` of subscriber inside the variable sub
    subscription_path = None
    pass  # YOUR CODE HERE

    with subscriber:
        # use the method `subscribe` to create the subscriber with the `callback` function triggered at each message
        streaming_pull_future = None
        pass  # YOUR CODE HERE

        print(f"Listening for messages on {subscription_path}...\n")

        # streaming_pull_future is a Thread in background that listens to Pub/sub.
        # To await the future callback, the method `result` needs to be called
        try:
            streaming_pull_future.result()
        except TimeoutError:
            streaming_pull_future.cancel()


if __name__ == "__main__":
    project_id = os.environ["PROJECT_ID"]
    subscription_name = os.environ["SUBSCRIPTION_NAME"]

    try:
        run(subscription_name, project_id)
    except KeyboardInterrupt:
        # Stop gracefully on KeyboardInturrupt
        print("Interrupted : Stopped Subscribing messages")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
