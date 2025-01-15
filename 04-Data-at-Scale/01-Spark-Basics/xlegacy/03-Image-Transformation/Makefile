include ../../../make.inc

# Update the tag to 0.2 once the lwface/pages/Webcam.py code has been activated
TAG=lewagon/imgtransform:0.1

# Insert the Docker registry prefix here, remove the trailing slash /
REGISTRYPREFIX=

# Run the tests
test: pytest-and-write-output

# Run the application locally
run:
	poetry run streamlit run lwface/Home.py --server.address 0.0.0.0 --server.port 8080

# Prepare the docker "build" step
prep-build:
	@rm -rf build/
	@mkdir -p build/common/
	@cp -R ../../../common/lewagonde/ build/common/lewagonde/
	@echo "Copied common/lewagonde to build/common/lewagonde"

# Build the Docker image
build: prep-build
	docker build -t $(TAG) .

# Tag the Docker image with the Docker registry prefix
tag:
	docker tag $(TAG) $(REGISTRYPREFIX)/$(TAG)

# Push the image to your remote Docker registry
push:
	docker push $(REGISTRYPREFIX)/$(TAG)
