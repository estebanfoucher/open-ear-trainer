# Multi-stage build for production deployment
FROM node:18-alpine AS frontend-build

# Set working directory
WORKDIR /app/frontend

# Copy package files
COPY ../frontend/package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy frontend source
COPY ../frontend/ ./

# Build frontend
RUN npm run build

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
COPY ../pyproject.toml ./
COPY ../README.md ./

# Install Python dependencies
RUN uv venv && \
    . .venv/bin/activate && \
    uv pip install -e ".[dev]"

# Copy backend source
COPY ../backend/ ./backend/

# Copy soundfonts
COPY ../soundfonts/ ./soundfonts/

# Copy built frontend from previous stage
COPY --from=frontend-build /app/frontend/build ./frontend/build

# Create media and logs directories
RUN mkdir -p media/audio logs

# Collect static files (using development settings to avoid database issues)
RUN cd backend && \
    . ../.venv/bin/activate && \
    DJANGO_SETTINGS_MODULE=config.settings.development python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/exercises/ || exit 1

# Run the application
CMD ["sh", "-c", "cd backend && . ../.venv/bin/activate && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
