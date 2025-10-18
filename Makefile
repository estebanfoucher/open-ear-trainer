.PHONY: help install setup run run-backend run-frontend test lint format migrate clean

# Default target
help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Installation
install: ## Install all dependencies
	.venv/bin/activate && uv pip install -e ".[dev]"
	cd frontend && npm install

setup: install setup-env ## Full project setup
	uv venv
	.venv/bin/activate && uv pip install -e ".[dev]"
	cd frontend && npm install
	pre-commit install
	@echo "Download a SoundFont file (.sf2) to soundfonts/ directory"
	@echo "Set SOUNDFONT_PATH in .env file"

setup-env: ## Create .env file from template
	@if [ ! -f .env ]; then \
		echo "📝 Creating .env file from development template..."; \
		cp env.development.example .env; \
		echo "✅ .env file created! Edit it with your configuration."; \
	else \
		echo "⚠️  .env file already exists. Skipping creation."; \
	fi

# Development servers
run: ## Run both backend and frontend concurrently
	@echo "Starting backend and frontend servers..."
	@trap 'kill %1; kill %2' INT; \
	$(MAKE) run-backend & \
	$(MAKE) run-frontend & \
	wait

run-backend:
	source .venv/bin/activate && PYTHONPATH=/Users/estebanfoucher/workspace/open-ear-trainer/backend DJANGO_SETTINGS_MODULE=config.settings.development python backend/manage.py runserver

run-frontend: ## Run React development server
	cd frontend && npm start

# Code quality
lint: ## Run ruff linting
	ruff check backend/

format: ## Run ruff formatting
	ruff format backend/

type-check: ## Run type checking with ty
	uv run ty check backend/

# Testing
test: ## Run all tests
	.venv/bin/activate && pytest backend/tests/ -v

test-unit: ## Run unit tests only
	.venv/bin/activate && pytest backend/tests/ -v -m "not integration"

test-integration: ## Run integration tests only
	.venv/bin/activate && pytest backend/tests/ -v -m integration

test-coverage: ## Run tests with coverage report
	.venv/bin/activate && pytest backend/tests/ --cov=backend --cov-report=html --cov-report=term-missing

# Database
migrate:
	source .venv/bin/activate && cd backend && PYTHONPATH=/Users/estebanfoucher/workspace/open-ear-trainer/backend DJANGO_SETTINGS_MODULE=config.settings.development python manage.py migrate

# Cleanup
clean: ## Clean cache files and generated content
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf backend/.pytest_cache/
	rm -rf backend/htmlcov/
	rm -rf backend/.coverage
	rm -rf media/audio/
	rm -rf frontend/build/
	rm -rf frontend/node_modules/.cache/

clean-audio: ## Clean generated audio files
	rm -rf media/audio/

# Docker (optional)
docker-build: ## Build Docker image
	docker build -f docker/Dockerfile -t open-ear-trainer .

docker-run: ## Run with Docker (production)
	docker-compose -f docker/docker-compose.yml up

docker-run-dev: ## Run with Docker (development)
	docker-compose -f docker/docker-compose.dev.yml up

docker-run-prod: ## Run with Docker (production)
	docker-compose -f docker/docker-compose.prod.yml up

docker-clean: ## Clean up Docker resources
	docker/scripts/cleanup.sh

# Production
build-frontend: ## Build React app for production
	cd frontend && npm run build

collect-static: ## Collect Django static files
	cd backend && python manage.py collectstatic --noinput

# Deployment
deploy: ## Deploy using CLI script
	python deploy.py full

deploy-docker: ## Deploy with Docker
	python deploy.py docker

deploy-github: ## Deploy frontend to GitHub Pages
	python deploy.py github-pages

deploy-railway: ## Deploy backend to Railway
	python deploy.py railway

deploy-test: ## Run deployment tests
	python deploy.py test

deploy-lint: ## Run deployment linting
	python deploy.py lint

# Development helpers
shell: ## Open Django shell
	.venv/bin/activate && cd backend && python manage.py shell

superuser: ## Create Django superuser
	.venv/bin/activate && cd backend && python manage.py createsuperuser

check: ## Run all checks (lint, format, type-check, test)
	$(MAKE) lint
	$(MAKE) format
	$(MAKE) type-check
	$(MAKE) test-unit

pre-commit: ## Run pre-commit hooks on all files
	uv run pre-commit run --all-files

pre-commit-install: ## Install pre-commit hooks
	uv run pre-commit install
