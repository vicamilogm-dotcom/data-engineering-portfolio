import re

import dockerfile
import pytest


class TestTask3:
    @pytest.fixture
    def dockerfile_validation_1(self):
        return {
            "FROM": "python:3.8.10",
            "ARG": "DEBIAN_FRONTEND=noninteractive",
            "ENV": "PYTHONUNBUFFERED 1",
            "RUN": (
                "apt-get -y update "
                "&& apt-get -y upgrade "
                "&& pip install --no-cache-dir poetry "
                "&& poetry install --only main "
                "&& apt-get clean "
                "&& rm -rf /var/lib/apt/lists/*"
            ),
            "WORKDIR": "/server",
            "COPY": "./ ./",
            "EXPOSE": "8000",
            "ENTRYPOINT": "uvicorn",
            "CMD": "app.main:app --host 0.0.0.0 --port 8000",
        }

    @pytest.fixture
    def dockerfile_validation_2(self):
        return {
            "FROM": "python:3.8.10-slim",
            "ARG": "DEBIAN_FRONTEND=noninteractive",
            "ENV": "PYTHONUNBUFFERED 1",
            "RUN": (
                "apt-get -y update "
                "&& apt-get -y upgrade "
                "&& pip install --no-cache-dir poetry "
                "&& poetry install --only main "
                "&& apt-get clean "
                "&& rm -rf /var/lib/apt/lists/*"
            ),
            "WORKDIR": "/server",
            "COPY": "./ ./",
            "EXPOSE": "8000",
            "ENTRYPOINT": "uvicorn",
            "CMD": "app.main:app --host 0.0.0.0 --port 8000",
        }

    @pytest.mark.skip(reason="Can be too rigid")
    def test_dockerfile_task_3_1(self, dockerfile_validation_1):
        dockerfile_name = "dockerfile-task-3-1"
        dockerfile_parsed = dockerfile.parse_file(dockerfile_name)

        for command in dockerfile_parsed:
            # Checks key is present in dictionnary
            assert command.cmd in dockerfile_validation_1
            # if we have the same instructions repeated in the dockerfile, value is stored as a list:
            if command.cmd == "RUN":
                s = re.sub(r"\s+", " ", command.value[0])
                assert s == dockerfile_validation_1.get(command.cmd)
            else:
                assert " ".join(command.value) == dockerfile_validation_1.get(
                    command.cmd
                )

    def test_dockerfile_task_3_1_keys_only(self):
        dockerfile_name = "dockerfile-task-1"
        dockerfile_parsed = dockerfile.parse_file(dockerfile_name)

        keys_to_check = [
            "FROM",
            "ARG",
            "ENV",
            "RUN",
            "WORKDIR",
            "COPY",
            "EXPOSE",
            "ENTRYPOINT",
            "CMD",
        ]
        for command in dockerfile_parsed:
            # Checks key is present in dictionnary
            assert command.cmd in keys_to_check

    @pytest.mark.skip(reason="Can be too rigid")
    def test_dockerfile_task_3_2(self, dockerfile_validation_2):
        dockerfile_name = "dockerfile-task-3-2"
        dockerfile_parsed = dockerfile.parse_file(dockerfile_name)

        for command in dockerfile_parsed:
            # Checks key is present in dictionnary
            assert command.cmd in dockerfile_validation_2
            # if we have the same instructions repeated in the dockerfile, value is stored as a list:
            if command.cmd == "RUN":
                s = re.sub(r"\s+", " ", command.value[0])
                assert s == dockerfile_validation_2.get(command.cmd)
            else:
                assert " ".join(command.value) == dockerfile_validation_2.get(
                    command.cmd
                )

    def test_dockerfile_task_3_2_keys_only(self):
        dockerfile_name = "dockerfile-task-1"
        dockerfile_parsed = dockerfile.parse_file(dockerfile_name)

        keys_to_check = [
            "FROM",
            "ARG",
            "ENV",
            "RUN",
            "WORKDIR",
            "COPY",
            "EXPOSE",
            "ENTRYPOINT",
            "CMD",
        ]
        for command in dockerfile_parsed:
            # Checks key is present in dictionnary
            assert command.cmd in keys_to_check
