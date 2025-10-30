# /backend/Dockerfile
# syntax=docker/dockerfile:1.7-labs
# ^ BuildKit syntax (enables mount caching & parallel layer builds)

# ------------------------------------------------------------
# Stage 1: Base configuration and dependency install
# ------------------------------------------------------------
# Use the official NVIDIA PyTorch image as the base.
# It already includes Python, PyTorch, and CUDA drivers.
# The `AS base` alias allows subsequent stages to reference this base image.
FROM nvcr.io/nvidia/pytorch:23.09-py3 AS base

# System settings
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /

# The NVIDIA PyTorch image already has many system dependencies.
# The following apt-get line is likely no longer necessary, but is kept
# in case you need other specific tools (e.g., git).
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Create a non-privileged user
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# ------------------------------------------------------------
# Stage 2: Install dependencies with caching
# ------------------------------------------------------------
FROM base AS deps

# Use BuildKit mounts for caching and bind-mounting requirements.txt
# This ensures that pip downloads are cached and only rebuilt when requirements.txt changes.
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    pip install -r requirements.txt

# ------------------------------------------------------------
# Stage 3: Final runtime image
# ------------------------------------------------------------
FROM base AS final

WORKDIR /app

# Copy installed site-packages from deps layer for speed
COPY --from=deps /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=deps /usr/local/bin /usr/local/bin

# Copy app code
COPY . .

# Ensure appuser owns the application files and instance directory
RUN mkdir -p /app/instance && chown -R appuser:appuser /app

# Switch to non-root user for safety
USER appuser

# Expose port 8000 for app access
EXPOSE 8000

# ------------------------------------------------------------
# CMD for development
# ------------------------------------------------------------

# --- For Gunicorn (production-style dev) ---
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:create_app()"]