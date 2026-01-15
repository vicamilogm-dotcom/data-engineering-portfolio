FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --no-cache-dir poetry

# Instala SOLO dependencias (sin instalar el proyecto todavía)
COPY pyproject.toml poetry.lock* /app/
RUN poetry config virtualenvs.create false \
 && poetry install --no-interaction --no-ansi --no-root

# Ahora sí copia el código
COPY . /app

EXPOSE 8080

CMD ["sh","-c","uvicorn twitter_api.main:app --host 0.0.0.0 --port ${PORT:-8080}"]
