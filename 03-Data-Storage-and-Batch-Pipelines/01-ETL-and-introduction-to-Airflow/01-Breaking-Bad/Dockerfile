FROM python:3.12.8-slim

ARG DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Airflow home
ENV AIRFLOW_HOME=/app/airflow
WORKDIR ${AIRFLOW_HOME}

# Copy airflow entrypoint scripts
COPY scripts ./scripts
RUN chmod +x ./scripts/entrypoint.sh

# Install dependencies via Poetry (no dev)
COPY pyproject.toml poetry.lock ./
RUN python -m pip install --no-cache-dir -U pip \
  && python -m pip install --no-cache-dir poetry \
  && poetry install --without dev --no-interaction --no-ansi
