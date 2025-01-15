include ../../../make.inc

.PHONY: install test testTask1 testTask2 testTask3

prepTest1:
	docker compose -f docker-compose-1.yml config

testTask1:
	PYTHONDONTWRITEBYTECODE=1 pytest -v --color=yes -k TestTask1

prepTask2:
	docker compose -f docker-compose-2.yml config

testTask2:
	PYTHONDONTWRITEBYTECODE=1 pytest -v --color=yes -k TestTask2

prepTask3:
	docker compose -f docker-compose-3.yml config

testTask3:
	PYTHONDONTWRITEBYTECODE=1 pytest -v --color=yes -k TestTask3

test: pytest-and-write-output
