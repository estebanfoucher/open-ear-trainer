# Simple Dockerfile for Railway deployment
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=config.settings.production
ENV PORT=8000

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libfluidsynth-dev \
    fluid-soundfont-gm \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install uv
RUN pip install uv

# Copy project files
COPY pyproject.toml ./
COPY README.md ./

# Install Python dependencies
RUN uv venv && \
    . .venv/bin/activate && \
    uv pip install -e ".[dev]"

# Copy backend source
COPY backend/ ./backend/

# Copy soundfonts
COPY soundfonts/ ./soundfonts/

# Create media directory
RUN mkdir -p media/audio

# Expose port
EXPOSE $PORT

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:$PORT/api/exercises/ || exit 1

# Run the application
CMD ["sh", "-c", "cd backend && . ../.venv/bin/activate && python manage.py migrate && python manage.py runserver 0.0.0.0:$PORT"]
