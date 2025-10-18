# Python backend stage
FROM python:3.11-slim AS backend

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=config.settings.production
ENV DOCKER=true

# Install system dependencies with retry and fix-missing
RUN apt-get update --fix-missing \
    && apt-get install -y --no-install-recommends --fix-missing \
        build-essential \
        libfluidsynth-dev \
        fluid-soundfont-gm \
        curl \
    && rm -rf /var/lib/apt/lists/* \
    || (apt-get update --fix-missing && apt-get install -y --no-install-recommends --fix-missing build-essential libfluidsynth-dev fluid-soundfont-gm curl && rm -rf /var/lib/apt/lists/*)

# Set working directory
WORKDIR /app

# Install uv
RUN pip install uv

# Copy Python dependencies and README
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

# Frontend is deployed separately to GitHub Pages

# Create media and logs directories
RUN mkdir -p media/audio logs

# Collect static files (using development settings to avoid database issues)
RUN cd backend && \
    . ../.venv/bin/activate && \
    DJANGO_SETTINGS_MODULE=config.settings.development python manage.py collectstatic --noinput

# Expose port (Railway will inject PORT env var)
EXPOSE $PORT

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8000}/health/ || exit 1

# Run the application
CMD ["sh", "-c", "cd backend && . ../.venv/bin/activate && python manage.py migrate && python manage.py runserver 0.0.0.0:${PORT:-8000}"]
