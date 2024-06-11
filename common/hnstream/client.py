"""
Example client code
"""

from __future__ import print_function

import argparse
import logging

import grpc

from hnstream.pyproto import server_pb2, server_pb2_grpc


def run(host: str, q: str = "comments", unix_time: int = 0, limit: int = 20):
    """
    Example
    """
    assert q in ["stories", "comments"]
    with grpc.insecure_channel(host) as channel:
        stub = server_pb2_grpc.HnstreamerStub(channel)
        if q == "stories":
            response = stub.GetNextStories(
                server_pb2.GetNextRequest(unix_time=unix_time, limit=limit)
            )
            print(response)
        else:
            response = stub.GetNextComments(
                server_pb2.GetNextRequest(unix_time=unix_time, limit=limit)
            )
            print(response)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", default="stories")
    parser.add_argument("--host", default="localhost:50051")
    parser.add_argument("--unix_time", type=int, default=0)
    parser.add_argument("--limit", type=int, default=20)
    return parser.parse_args()


if __name__ == "__main__":
    logging.basicConfig()
    _args = parse_args()
    run(q=_args.q, host=_args.host, unix_time=_args.unix_time, limit=_args.limit)
