# Simple, single-stage image of the praktikum-llm package (week 4 replaces the multi-stage build from week 3).
#   docker build -t praktikum-llm .
#   docker run --rm praktikum-llm --version
FROM python:3.13-alpine

# PYTHONDONTWRITEBYTECODE: do not write .pyc files; PYTHONUNBUFFERED: logs appear immediately.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Editable install: the `llm` command runs the code from /app/src, so a bind mount on /app
# (step 3 of the exercise) changes the running code without a rebuild.
COPY pyproject.toml version.txt ./
COPY src/ src/
RUN pip install --no-cache-dir -e .

ENTRYPOINT ["llm"]
CMD ["--help"]
