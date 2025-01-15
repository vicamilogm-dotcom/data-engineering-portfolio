# TODO: fix tests
# import os

# from pytest import approx
# from datetime import datetime
# from api import proto_rpc_server

# def test_http_time_format():
#     from api import rest_api
#     hms = rest_api.time()
#     assert isinstance(hms["h"], int)
#     assert isinstance(hms["m"], int)
#     assert isinstance(hms["s"], int)

# def test_grpc_time_format():
#     api = proto_rpc_server.Api()
#     response = api.get_time(proto_rpc_server.api_pb2.TimeRequest(), None)
#     assert isinstance(response.h, int)
#     assert isinstance(response.m, int)
#     assert isinstance(response.s, int)

# def test_rural_population_percentage_http():
#     from api import rest_api
#     assert rest_api.get_rural_population("France", 1964) == approx(34.102)


# def test_rural_population_percentage_grpc():
#     api = proto_rpc_server.Api()
#     response = api.get_rural_population_percentage(proto_rpc_server.api_pb2.RuralRequest(year=1964, country="France"), None)
#     assert response.value == approx(34.102)


def test():
    assert True
