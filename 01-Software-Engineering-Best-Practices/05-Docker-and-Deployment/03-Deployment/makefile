

# Cargar variables del archivo .env
include .env
export $(shell sed 's/=.*//' .env)

build_docker_image:
	@echo ">>> Building Docker image: $(DOCKER_IMAGE_NAME)"
	docker build -t $(DOCKER_IMAGE_NAME) .

run_docker_image:
	@echo ">>> Running Docker image: $(DOCKER_IMAGE_NAME) on port $(PORT)"
	docker run --rm -p $(PORT):$(PORT) -e PORT=$(PORT) $(DOCKER_IMAGE_NAME)

push_docker_image:
	@echo ">>> Pushing Docker image: $(DOCKER_IMAGE_NAME)"
	docker push $(DOCKER_IMAGE_NAME)

deploy_docker_image:
	@echo ">>> Deploying to Cloud Run"
	gcloud run deploy fastapi-deployment \
		--image=$(DOCKER_IMAGE_NAME) \
		--platform=managed \
		--region=us-central1 \
		--allow-unauthenticated \
		--port=$(PORT)

