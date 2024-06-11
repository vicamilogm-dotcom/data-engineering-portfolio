import logging
from concurrent import futures

import grpc

from hnstream import bq, queries
from hnstream.pyproto import server_pb2, server_pb2_grpc


class Hnstreamer(server_pb2_grpc.HnstreamerServicer):
    def __init__(self) -> None:
        super().__init__()
        self.client = bq.get_client()

    def GetNextStories(
        self, request: server_pb2.GetNextRequest, _context
    ) -> server_pb2.GetNextStoriesResponse:
        stories_after_query, stories_after_params = queries.stories_after(
            unix_time=request.unix_time, limit=request.limit
        )
        stories_list = bq.query_as_list(
            self.client, stories_after_query, query_parameters=stories_after_params
        )
        response = server_pb2.GetNextStoriesResponse()

        for story_dict in stories_list:
            story = response.stories.add()
            for k, v in story_dict.items():
                if hasattr(story, k):
                    setattr(story, k, v)

        return response

    def GetNextComments(
        self, request: server_pb2.GetNextRequest, _context
    ) -> server_pb2.GetNextCommentsResponse:
        comments_after_query, comments_after_params = queries.comments_after(
            unix_time=request.unix_time, limit=request.limit
        )
        comments_list = bq.query_as_list(
            self.client, comments_after_query, query_parameters=comments_after_params
        )
        response = server_pb2.GetNextCommentsResponse()

        for comment_dict in comments_list:
            comment = response.comments.add()
            for k, v in comment_dict.items():
                if hasattr(comment, k):
                    setattr(comment, k, v)

        return response


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    server_pb2_grpc.add_HnstreamerServicer_to_server(Hnstreamer(), server)
    port = 50051
    server.add_insecure_port(f"[::]:{port}")
    print(f"Starting gRPC server on port {port}")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()
