from api.generated_proto import api_pb2
from api.generated_proto import api_pb2_grpc

import grpc
from concurrent import futures
import datetime


class TimeService(api_pb2_grpc.TimeServiceServicer):
    def GetTime(self, request, context):
        # write the logic for the GetTime() method
        pass  # YOUR CODE HERE


# Create a gRPC server and add your TimeService to it!
pass  # YOUR CODE HERE

server.add_insecure_port("[::]:50052")
server.start()
print("server started running")
server.wait_for_termination()
