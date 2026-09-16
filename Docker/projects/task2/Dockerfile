# --------------- Stage 1: Build ------------------
    FROM python:3.12-slim-bullseye AS builder
    WORKDIR /build

# Install build tools needed to compile python deps
    RUN apt-get update && apt-get install -y --no-install-recommends \
        gcc \
        && rm -rf /var/lib/apt/lists/*

# Install dependencies into a local folder
    COPY requirements.txt .
    RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# --------------- Stage 2: Runtime ------------------
    FROM python:3.12-slim AS runtime

# Crreate a non-root user (security best practice)
    RUN useradd --create-home --shell /bin/bash appuser

    WORKDIR /app

# Copy the installed dependencies from the builder stage
    COPY --from=builder /install /usr/local

# Copy the application code
    COPY app.py .

# Enviroment variables (secure defaults; override in runtime)
    ENV APP_NAME="ProgreeApp" \
        APP_ENV="production" \
        PORT="6767" \
        PYTHONUNBUFFERED=1

# Run as non-root user
    USER appuser

# Document the port the container will listen on
    EXPOSE 6767

# Start the application
    CMD ["gunicorn", "--bind", "0.0.0:6767", "app:app"]
