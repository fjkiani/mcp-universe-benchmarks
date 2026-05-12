# Multi-stage Dockerfile for FastAPI Backend + Governance Engine
# Supports DEMO_MOCK_MODE=true (no CLI needed) and live mode with lbx_cli

FROM python:3.11-slim

WORKDIR /app

# Install build + runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip to avoid old resolver issues
RUN pip install --no-cache-dir --upgrade pip

# Install Python dependencies directly
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn==21.2.0

# Copy backend source code
COPY . .

# Set environment variables for production
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
# Default port to 8000 (Render injects $PORT dynamically)
ENV PORT=8000
# Governance Engine mode — set to false in Render dashboard for live certifications
ENV DEMO_MOCK_MODE=true
# PYTHONPATH for domain evaluators and backend module resolution
ENV PYTHONPATH=/app

# Expose the API port
EXPOSE $PORT

# Run using Gunicorn with Uvicorn workers for production scaling
CMD gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
