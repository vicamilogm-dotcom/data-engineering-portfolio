import os
import pathlib

import yaml


def test_docker_compose():
    parent_dir = pathlib.Path(os.path.realpath(__file__)).parent.parent
    dc_fp = os.path.join(parent_dir, "docker-compose.yml")
    with open(dc_fp) as f:
        dc = yaml.safe_load(f)
    neo4j_services = [
        service
        for service in dc["services"].values()
        if service["image"].startswith("neo4j:")
    ]
    assert len(neo4j_services) == 1, "Neo4j not found in the docker-compose.yml"

    if len(neo4j_services) == 1:
        service = neo4j_services[0]
        assert len(service["environment"]) >= 1
        assert len(service["ports"]) >= 2


# def test_dgraph():
#     parent_dir = pathlib.Path(os.path.realpath(__file__)).parent.parent
#     dc_fp = os.path.join(parent_dir, "docker-compose.yml")
#     with open(dc_fp) as f:
#         dc = yaml.safe_load(f)
#     dgraph_services = [
#         service
#         for service in dc["services"].values()
#         if service["image"].startswith("dgraph")
#     ]
#     assert (
#         len(dgraph_services) == 3
#     ), "DGraph services not found in the docker-compose.yml"
