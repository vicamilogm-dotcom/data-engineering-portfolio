import grpc
from api.generated_proto import api_pb2
from api.generated_proto import api_pb2_grpc
import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--country", required=True, help="Country Name")
    parser.add_argument("--year", required=True, help="Year")
    return parser.parse_args()


def run_client(country: str, year: str):
    # Create a gRPC channel
    pass  # YOUR CODE HERE


if __name__ == "__main__":
    args = parse_args()
    run_client(args.country, args.year)
