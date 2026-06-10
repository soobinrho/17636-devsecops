# Reference: https://docs.astral.sh/uv/guides/integration/fastapi/#deployment
FROM python:3.14-slim
EXPOSE 80/tcp

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
COPY . /app
WORKDIR /app
RUN uv sync --frozen --no-cache
CMD ["/app/.venv/bin/fastapi", "run", "app/main.py", "--port", "80", "--host", "0.0.0.0", "--forwarded-allow-ips", "'*'"]