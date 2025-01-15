FROM python:3.12.8-slim

# Setting PYTHONUNBUFFERED to 1 is useful for logs
# See https://stackoverflow.com/a/59812588
ENV PYTHONUNBUFFERED=1

# Set a working directory that maps our data-engineering-challenges repository structure
WORKDIR /repo/02-Data-at-Scales/04-Large-DB/05-Recap/

# Install Poetry
RUN pip3 install --upgrade --no-cache-dir pip \
    && pip3 install poetry

# Copy the installation files and local dependencies first (in this case there aren't local dependencies)
COPY poetry.lock pyproject.toml ./

# Now we are ready to install the packages
RUN poetry install --only main

# Copy this package's Python files last
COPY ./ ./

# Set a default PORT environment variable to 8080
ENV PORT 8080

# Run the `FastAPI` application on port 8080
CMD poetry run uvicorn lwserverless.app:app --host 0.0.0.0 --port $PORT
