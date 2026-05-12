# Root-level Dockerfile for Render dashboard deployments
# Context: repo root (Render default)

FROM python:3.11-slim

WORKDIR /app

# Install build + runtime dependencies in one layer
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip to avoid old resolver issues
RUN pip install --no-cache-dir --upgrade pip

# Install Python dependencies directly (no wheel stage)
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn==21.2.0

# Copy backend source into /app
COPY backend/ .

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PORT=8000
ENV DEMO_MOCK_MODE=true
ENV PYTHONPATH=/app

EXPOSE $PORT

CMD gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
