FROM python:3.12-slim

WORKDIR /app

# Instalar dependencias del sistema (útil para compilar algunas libs)
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# Copiar archivos de Poetry / dependencias
COPY pyproject.toml poetry.lock* ./

# Instalar Poetry y dependencias del proyecto (sin entorno virtual)
RUN pip install --upgrade pip && pip install "poetry==2.2.1" \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Copiar el resto del código
COPY . .

# Puerto por defecto (para local)
ENV PORT=8000

# Exponer el puerto (informativo)
EXPOSE 8000

# Comando de arranque usando la variable de entorno PORT
CMD uvicorn app.main:app --host 0.0.0.0 --port $PORT
