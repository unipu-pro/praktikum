# Simple, single-stage image of the llm CLI (week 4 replaces the multi-stage build from week 3).
#   docker build -t praktikum-llm .
#   docker run --rm praktikum-llm --version
FROM python:3.13-alpine

# PYTHONDONTWRITEBYTECODE: do not write .pyc files; PYTHONUNBUFFERED: logs appear immediately.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Dependencies first: this layer is rebuilt only when requirements.txt changes.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Source code last: it changes most often.
COPY version.txt ollama_client.py llm.py ./

ENTRYPOINT ["python", "llm.py"]
CMD ["--help"]
