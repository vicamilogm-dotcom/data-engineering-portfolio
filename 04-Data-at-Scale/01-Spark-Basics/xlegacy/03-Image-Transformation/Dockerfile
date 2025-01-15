# Start from Python 3.8.10, the slim version is usually enough (stripped from packages that aren't useful for our purpose)
# and way smaller than the non-slim version
FROM python:3.8.10-slim

# Setting PYTHONUNBUFFERED to 1 is useful for logs
# See https://stackoverflow.com/a/59812588
ENV PYTHONUNBUFFERED 1

# Install Ubuntu dependencies for our various fancy image transformation packages
RUN apt-get update -y && \
  apt-get -y install ffmpeg libsm6 libxext6 libgl1-mesa-glx libopencv-dev

# Set a working directory that maps our data-engineering-challenges repository structure
# so that relative imports like ../../../common/lewagonde work within the Docker image
WORKDIR /repo/02-Data-at-Scales/02-Data-transformation/02-Image-Transformation/

# Install Poetry
RUN pip3 install --upgrade --no-cache-dir pip \
    && pip3 install poetry

# Copy the installation files and local dependencies first
COPY poetry.lock pyproject.toml ./
COPY build/common/lewagonde/ /repo/common/lewagonde/

# Now we are ready to install the packages
RUN poetry install --only main

# Copy this package's Python files last
COPY ./ ./

# Set the PORT to 8080 but allow overriding
ENV PORT 8080

# Run the `streamlit run` command on port 8080
CMD poetry run streamlit run lwface/Home.py --server.address 0.0.0.0 --server.port $PORT

# --> Delete this line when you've read the full Dockerfile, so the `test_dockerfile` test passes ;)
