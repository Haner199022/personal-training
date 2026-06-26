# syntax=docker/dockerfile:1
# Personal-Training API — production image
# Base pinned to a specific minor (never :latest) for reproducible builds.
FROM python:3.12-slim AS base

# --- runtime env ---
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# --- system deps ---
# curl: used by the container HEALTHCHECK to hit /api/v1/health.
# psycopg[binary] ships its own libpq, so no libpq-dev needed at runtime.
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# --- python deps (cached layer: only re-runs when requirements.txt changes) ---
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir "gunicorn==23.0.*"

# --- app source ---
COPY app ./app
# alembic migrations + config (run via `docker compose exec api alembic upgrade head`)
COPY alembic ./alembic
COPY alembic.ini ./alembic.ini

# --- non-root user ---
RUN useradd --create-home --uid 10001 appuser \
    && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# Health check hits the v1 health route exposed by app.api.v1.health.
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD curl -fsS http://localhost:8000/api/v1/health || exit 1

# gunicorn process manager + uvicorn ASGI workers.
# 4C8G single host -> 4 workers (2*CPU is too many for sync-blocking PG calls under async).
# Tune via WEB_CONCURRENCY env if needed.
CMD ["gunicorn", "app.main:app", \
     "--worker-class", "uvicorn.workers.UvicornWorker", \
     "--workers", "4", \
     "--bind", "0.0.0.0:8000", \
     "--timeout", "60", \
     "--graceful-timeout", "30", \
     "--access-logfile", "-", \
     "--error-logfile", "-"]
