# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1 \
  FLASK_APP=app.py

# Install system dependencies
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
  gcc \
  python3-dev \
  && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy public folder (poster images) first for better layer caching
COPY public/ ./public/

# Copy application files explicitly
COPY app.py .
COPY templates/ ./templates/

# Create a non-root user and switch to it
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 5000

# Command will be overridden by docker-compose
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"] 