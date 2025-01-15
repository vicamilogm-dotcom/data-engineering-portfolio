include ../../../make.inc

.PHONY: install test testTask1 testTask2 testTask3

# Build tasks
buildTask1:
	docker build -t base-image-fastapi-ubuntu-fat:test -f dockerfile-task-1 .

buildTask2:
	docker build -t base-image-fastapi-ubuntu:test -f dockerfile-task-2 .

buildTask3-1:
	docker build -t base-image-fastapi-fat:dev -f dockerfile-task-3-1 .

buildTask3-2:
	docker build -t base-image-fastapi:dev -f dockerfile-task-3-2 .

buildTask-non-root:
	docker build -t nonroot-image-fastapi:dev -f dockerfile-task-3-2 .


# Run tasks
runTask1:
	docker run --rm -it -p 8000:8000 base-image-fastapi-ubuntu-fat:test

runTask2:
	docker run --rm -it -p 8000:8000 base-image-fastapi-ubuntu:test

runTask3-1:
	docker run --rm -it -p 8000:8000 base-image-fastapi-fat:dev

runTask3-2:
	docker run --rm -it -p 8000:8000 base-image-fastapi:dev

runTask-non-root:
	docker run --rm -it -p 8000:8000 nonroot-image-fastapi:dev

# Test Tasks
test: pytest-and-write-output

testTask1: buildTask1
	PYTHONDONTWRITEBYTECODE=1 poetry run pytest -v --color=yes -k TestTask1

testTask2: buildTask2
	PYTHONDONTWRITEBYTECODE=1 poetry run pytest -v --color=yes -k TestTask2

testTask3-1: buildTask3-1
	PYTHONDONTWRITEBYTECODE=1 poetry run pytest -v --color=yes tests/test_task_3.py::TestTask3::test_dockerfile_task_3_1

testTask3-2: buildTask3-2
	PYTHONDONTWRITEBYTECODE=1 poetry run pytest -v --color=yes tests/test_task_3.py::TestTask3::test_dockerfile_task_3_2
