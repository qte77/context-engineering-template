# --- Build Stage ---
FROM python:3.13-slim-bookworm AS builder
WORKDIR /app

COPY pyproject.toml uv.lock README.md Makefile ./
COPY src ./src
COPY examples ./examples

RUN pip install uv -q
RUN uv sync --frozen

# --- Run Stage ---
FROM python:3.13-slim-bookworm AS runner
WORKDIR /app
ENV PYTHONPATH=/app/src

COPY --from=builder /app/src ./src
COPY --from=builder /app/examples ./examples
COPY pyproject.toml uv.lock ./

RUN chmod +x ./src/main.py
CMD ["python", "-m", "examples/main", "server"]
