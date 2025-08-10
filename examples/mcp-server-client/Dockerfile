# --- Build Stage ---
FROM python:3.13-slim-bookworm AS builder
WORKDIR /app

COPY pyproject.toml uv.lock ./
COPY src ./src

RUN pip install uv -q
RUN uv sync --frozen

# --- Run Stage ---
FROM python:3.13-slim-bookworm AS runner
WORKDIR /app
ENV PYTHONPATH=/app/src

COPY --from=builder /app/.venv ./.venv
COPY --from=builder /app/src ./src
COPY pyproject.toml uv.lock ./

ENV PATH="/app/.venv/bin:$PATH"
CMD ["python", "-m", "src.main", "server"]
