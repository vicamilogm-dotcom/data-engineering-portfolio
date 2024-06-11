import pytest
from yaml import load
from yaml.loader import SafeLoader


@pytest.mark.optional
class TestDockerCompose:
    def test_docker_compose(self):
        keys_to_check = [
            "webapi",
            "build",
            "context",
            "dockerfile",
            "restart",
            "ports",
            "volumes",
            "master",
            "worker",
            "env_file",
        ]

        def get_keys(d, keys=None):
            keys = keys or []
            if isinstance(d, dict):
                keys += d.keys()
                _ = [get_keys(x, keys) for x in d.values()]
            elif isinstance(d, list):
                _ = [get_keys(x, keys) for x in d]
            return list(set(keys))

        with open("docker-compose-task-2.yml") as f:
            docker_compose_data = load(f, SafeLoader)

            keys = get_keys(docker_compose_data)
            assert all(item in keys for item in keys_to_check)
