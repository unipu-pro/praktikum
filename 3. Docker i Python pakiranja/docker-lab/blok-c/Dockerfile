# syntax=docker/dockerfile:1
# Step 2: multi-stage build of the praktikum-llm package.
#   docker build -t praktikum-llm .               -> runtime image (default, last stage)
#   docker build --target test -t llm-test .      -> runs the tests during the build

ARG PYTHON_IMAGE=python:3.13-alpine

# ---- build: turn the source tree into a wheel ----
FROM ${PYTHON_IMAGE} AS build
WORKDIR /src
RUN pip install --no-cache-dir build
COPY pyproject.toml version.txt ./
COPY src/ src/
RUN python -m build --wheel --outdir /dist

# ---- test: install the wheel with dev extras and run pytest against it ----
FROM ${PYTHON_IMAGE} AS test
WORKDIR /src
COPY --from=build /dist/ /dist/
RUN pip install --no-cache-dir "$(ls /dist/*.whl)[dev]"
COPY pyproject.toml version.txt ./
COPY tests/ tests/
RUN python -m pytest -v

# ---- runtime: only the installed package, running as a non-root user ----
FROM ${PYTHON_IMAGE} AS runtime
# PYTHONDONTWRITEBYTECODE: do not write .pyc files; they only add size to the image layer.
# PYTHONUNBUFFERED: send stdout/stderr straight to the container log instead of buffering,
# so `docker logs` shows output immediately (and nothing is lost if the process is killed).
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
RUN adduser -D -u 10001 app
COPY --from=build /dist/ /tmp/dist/
RUN pip install --no-cache-dir /tmp/dist/*.whl && rm -rf /tmp/dist
USER app
WORKDIR /home/app
ENTRYPOINT ["llm"]
CMD ["--help"]
