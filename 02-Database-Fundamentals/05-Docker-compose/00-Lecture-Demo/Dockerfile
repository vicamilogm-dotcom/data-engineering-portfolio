FROM python:3.12.8-slim

ARG DEBIAN_FRONTEND=noninteractive

ENV PYTHONUNBUFFERED=1
ENV WRITEPYTHONBYTECODE=1

WORKDIR /app

COPY ./  ./

RUN apt-get update \
    && apt-get -y upgrade \
    && pip install --no-cache-dir poetry \
    && poetry install \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 8000

ENTRYPOINT [ "poetry", "run" ]

CMD ["uvicorn", "api.fast:app", "--host", "0.0.0.0", "--port", "8000"]
# For hot reloading with a bind mount
# CMD ["uvicorn", "api.fast:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
