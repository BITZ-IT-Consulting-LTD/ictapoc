# Production Backend Dockerfile
FROM python:3.11-slim

# System environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

WORKDIR /app

# Install system dependencies (Hardened: only minimal requirements)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY backend/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir gunicorn gevent setproctitle

# Copy project source
COPY ./backend /app/

# Create a non-privileged user and group
RUN groupadd -g 1000 appuser && \
    useradd -u 1000 -g appuser -s /bin/sh appuser

# Pre-prepare directories for volumes to ensure correct permissions
RUN mkdir -p /app/staticfiles /app/media && \
    chown -R appuser:appuser /app/staticfiles /app/media

# Switch to non-privileged user
USER appuser

# Expose the internal port
EXPOSE 8000

# Use Gunicorn with the hardware-optimized config
CMD ["gunicorn", "-c", "gunicorn_config.py", "project.wsgi:application"]
