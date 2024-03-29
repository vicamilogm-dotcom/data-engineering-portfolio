include ../../../make.inc
include .env

.PHONEY: submit-write-to-raw submit-staging-transform submit-create-processed test

UUID := $(shell uuidgen | tr '[:upper:]' '[:lower:]')

test: pytest-and-write-output

create-cluster:
	gcloud dataproc clusters create $(CLUSTER_NAME) \
		--project=$(PROJECT_ID) \
		--region=europe-west1 \
		--network=spark-vpc \
		--master-machine-type e2-standard-2 \
		--master-boot-disk-size 50 \
		--num-workers 2 \
		--worker-machine-type e2-standard-2 \
		--worker-boot-disk-size 50

destroy-cluster:
	gcloud dataproc clusters delete $(CLUSTER_NAME) \
		--project=$(PROJECT_ID) \
		--region=europe-west1 \
		--quiet


