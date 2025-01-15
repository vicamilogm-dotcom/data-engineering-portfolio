import grpc
from concurrent import futures
from api.generated_proto import api_pb2
from api.generated_proto import api_pb2_grpc
from api import rural


class CountryYearService(api_pb2_grpc.CountryYearServiceServicer):
    # Complete the method that will receive the data, transform it, and return it
    def GetCountryYear(self, request, context):
        pass  # YOUR CODE HERE


# Create a gRPC server ald add your CountryYearService to it
pass  # YOUR CODE HERE

server.add_insecure_port("[::]:50053")
server.start()
print("started running")
server.wait_for_termination()
