# Reference: https://docs.astral.sh/uv/guides/integration/fastapi/#deployment
FROM python:3.14-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
COPY . /app
WORKDIR /app
RUN uv sync --frozen --no-cache

# -u is required to force the stdout and stderr to be unbuffered.
# Source:
#   https://stackoverflow.com/a/29745541
ENTRYPOINT [".venv/bin/python", "-u", "app/main.py"]