import os

pass  # YOUR CODE HERE


def query_clickhouse(query):
    """
    Create a ClickHouse clinet and executes the passed query with the client.

    Returns:
    - Query results
    """
    pass  # YOUR CODE HERE


def get_all_messages():
    """
    Retrieves all messages from the user_messages table in ClickHouse.

    Returns:
    - list: A list containing all messages and their associated data.
    """
    query = ""
    pass  # YOUR CODE HERE
    return query_clickhouse(query)


def get_top_active_users():
    """
    Retrieves the top 5 active users based on message count from the user_messages table.

    Returns:
    - list: A list containing the usernames and their respective message counts, ordered by message count in descending order.
    """
    query = ""
    pass  # YOUR CODE HERE
    return query_clickhouse(query)


def get_average_message_gap():
    """
    Computes the average time gap (in seconds) between consecutive messages in the user_messages table.

    Returns:
    - list: A list containing the average time gap in seconds.
    """
    query = ""
    pass  # YOUR CODE HERE
    return query_clickhouse(query)


if __name__ == "__main__":
    from pprint import pprint as print

    print(get_average_message_gap())
