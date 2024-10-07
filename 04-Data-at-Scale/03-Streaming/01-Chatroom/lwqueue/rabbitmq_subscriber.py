import argparse
import datetime
import json
from typing import Callable, List, TypedDict

from rich.live import Live

from lwqueue import rabbitmq, message, ui

MODE_SIMPLE = "simple"
MODE_RICH = "rich"


class LiveParams(TypedDict):
    live: Live
    messages: List[message.Message]


def print_callback(channel: str, method, properties, body):
    """
    Very simple callback that just prints the body to the console
    """
    pass  # YOUR CODE HERE


def make_live_callback(live_params: LiveParams):
    """
    Returns a callback, ie. a function
    """

    def live_callback(channel: str, method, properties, body):
        parsed_body = json.loads(body)
        live_params["messages"].append(
            {**parsed_body, "received_at": str(datetime.datetime.utcnow())}
        )
        live_params["live"].update(ui.make_rich_table(live_params["messages"]))

    return live_callback


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

    result = channel.queue_declare(queue="chat", exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange=rabbitmq.EXCHANGE_NAME, queue=queue_name)

    print("[x] Waiting for messages. To exit, press CTRL+C")

    pass  # YOUR CODE HERE

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
    if args.mode == MODE_SIMPLE:
        receive_messages(
            host=args.host,
            port=args.port,
            on_message_callback=print_callback,
            rmq_username=args.rmq_username,
            rmq_password=args.rmq_password,
        )
    elif args.mode == MODE_RICH:
        empty_table = ui.make_rich_table([])
        messages: List[message.Message] = []
        with Live(empty_table, refresh_per_second=4) as live:
            receive_messages(
                host=args.host,
                port=args.port,
                on_message_callback=make_live_callback(
                    {"live": live, "messages": messages}
                ),
                rmq_username=args.rmq_username,
                rmq_password=args.rmq_password,
            )
    else:
        raise ValueError(f"Wrong --mode, only [{MODE_SIMPLE}, {MODE_RICH}] are valid")


if __name__ == "__main__":
    main()
