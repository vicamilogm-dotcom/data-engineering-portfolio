FROM python:3.12.8 AS builder

WORKDIR /tmp

# Required for poetry export without poetry plugins
RUN pip install poetry==1.8.5

COPY ./pyproject.toml ./poetry.lock ./

RUN poetry export --without-hashes --format=requirements.txt --output=requirements.txt

############################

FROM python:3.12.8-slim

# Create a system group GID `appgroup`
# adds new user `appuser` to `appgroup` with no home directory
RUN groupadd -r appgroup && useradd --no-log-init -r -g appgroup appuser

WORKDIR /app

COPY --from=builder /tmp/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY api api

RUN chown -R appuser:appgroup /app

ENV PATH="${PATH}:/app/.local/bin"

USER appuser

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Multi stage size: 177 MB
# Using poetry in single stage: 259 MB
# Poetry is quite heavy
