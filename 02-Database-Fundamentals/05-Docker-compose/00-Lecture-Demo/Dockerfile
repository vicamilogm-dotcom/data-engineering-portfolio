FROM python:3.12.8-slim

ARG DEBIAN_FRONTEND=noninteractive

ENV PYTHONUNBUFFERED=1
ENV WRITEPYTHONBYTECODE=1

WORKDIR /app
# Every Dockerfile directive is now relative to '/app' inside the image
# e.g. COPY can be interpreted as: COPY ./ /app/./
COPY ./  ./

RUN pip install --no-cache-dir poetry \
    && poetry install

EXPOSE 8000

ENTRYPOINT [ "poetry", "run" ]

CMD ["uvicorn", "api.fast:app", "--host", "0.0.0.0", "--port", "8000"]
