import argparse
import datetime
import json
import os
from typing import Callable, List, TypedDict

from rich.live import Live

from lwqueue import rabbitmq, message

pass  # YOUR CODE HERE


class LiveParams(TypedDict):
    live: Live
    messages: List[message.Message]


def clickhouse_callback(channel: str, method, properties, body):
    """
    Indexes a message into ClickHouse.

    This function takes in a message, augments it with the current UTC timestamp,
    and inserts the result into the `user_messages` table in a ClickHouse instance.
    It assumes a specific table structure and a specific set of columns.

    Parameters:
    - channel (str): The name of the channel through which the message is received.
    - method: The delivery method. This parameter is not used within the function
              but may be passed in by the calling function for compatibility with
              certain messaging protocols.
    - properties: Message properties. This parameter is not used within the function
                  but may be passed in by the calling function for compatibility with
                  certain messaging protocols.
    - body (bytes): The body of the message, typically in JSON format. It is expected
                    to be able to be parsed into a dictionary.

    The function expects the body to contain at least the 'username' and 'message' keys.
    It will add a 'received_at' key with the current UTC timestamp.

    The ClickHouse client connects to a local ClickHouse instance on port 9000 using
    the 'rmq' username. The password is fetched from an environment variable named
    "CLICKHOUSE_PASSWORD".

    Example:
    -------
    clickhouse_callback("my_channel", None, None, '{"username": "Alice", "message": "Hello, World!"}')

    This will insert a record into the `user_messages` table with the 'username' as 'Alice',
    'message' as 'Hello, World!', and 'received_at' as the current UTC timestamp.

    Note:
    -----
    Ensure that the ClickHouse server is running and the environment variable
    "CLICKHOUSE_PASSWORD" is set before calling this function.

    """
    parsed_body = json.loads(body)
    message_data = {**parsed_body, "received_at": datetime.datetime.now(datetime.UTC)}
    pass  # YOUR CODE HERE


def receive_messages(
    host: str,
    port: int,
    on_message_callback: Callable,
    rmq_username: str,
    rmq_password: str,
):
    """
    - Establish a connection to the RabbitMQ server
    - Connect to the exchange
    - Bind a queue to that exchange
    - Hook a callback and consume incoming messages
    - Close the connection
    """
    connection = rabbitmq.get_connection(
        host=host, port=port, username=rmq_username, password=rmq_password
    )
    channel = connection.channel()
    channel.exchange_declare(exchange=rabbitmq.EXCHANGE_NAME, exchange_type="fanout")

    result = channel.queue_declare(queue="clickhouse_insert", exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange=rabbitmq.EXCHANGE_NAME, queue=queue_name)

    print("[x] Waiting for messages. To exit, press CTRL+C")

    channel.basic_consume(
        queue=queue_name,
        on_message_callback=on_message_callback,
        auto_ack=True,
    )

    channel.start_consuming()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", required=True)
    parser.add_argument("--port", required=True, type=int)
    parser.add_argument("--mode", required=True)
    parser.add_argument("--rmq-username", required=True, help="RabbitMQ username")
    parser.add_argument("--rmq-password", required=True, help="RabbitMQ password")
    return parser.parse_args()


def main():
    args = parse_args()
    receive_messages(
        host=args.host,
        port=args.port,
        on_message_callback=clickhouse_callback,
        rmq_username=args.rmq_username,
        rmq_password=args.rmq_password,
    )


if __name__ == "__main__":
    main()
