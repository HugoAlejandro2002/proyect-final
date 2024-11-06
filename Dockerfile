FROM python:3.11-slim

# Dependencias para OpenCV
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y

# Copiar uv CLI desde una imagen externa
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Añadir el código fuente y otros archivos necesarios
ADD ./src /src
COPY pyproject.toml pyproject.toml
COPY uv.lock uv.lock

# Copiar los modelos y el PDF necesario
COPY model_artifacts /model_artifacts
COPY get-fit-life.pdf /get-fit-life.pdf

# Configurar el PIP_INDEX_URL para instalar PyTorch
ENV PIP_INDEX_URL=https://download.pytorch.org/whl/cpu

# Instalar dependencias usando uv
RUN uv sync --frozen --no-dev

# Comando de ejecución (sin las variables de entorno definidas directamente)
CMD uv run fastapi run src/main.py --host 0.0.0.0 --port ${PORT:-8000}
