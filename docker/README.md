# Docker Configuration

This directory contains all Docker-related configuration files for the Open Ear Trainer application.

## Structure

```
docker/
├── Dockerfile                 # Production Docker image
├── docker-compose.yml         # Base compose file
├── docker-compose.dev.yml     # Development environment
├── docker-compose.prod.yml    # Production environment
├── .dockerignore              # Docker ignore file
├── nginx/
│   ├── nginx.conf             # Base nginx configuration
│   ├── nginx.dev.conf         # Development nginx config
│   └── nginx.prod.conf        # Production nginx config
└── scripts/
    ├── build.sh               # Build script
    ├── deploy.sh              # Deployment script
    └── cleanup.sh             # Cleanup script
```

## Quick Start

### Development Environment
```bash
# Start development environment
docker/scripts/deploy.sh -e dev -a up

# Or using make
make docker-run-dev
```

### Production Environment
```bash
# Start production environment
docker/scripts/deploy.sh -e prod -a up

# Or using make
make docker-run-prod
```

### Build Custom Image
```bash
# Build with custom tag
docker/scripts/build.sh -t my-ear-trainer -p

# Or using make
make docker-build
```

## Scripts

### build.sh
Build Docker images with various options.

```bash
# Basic build
./docker/scripts/build.sh

# Build with custom tag
./docker/scripts/build.sh -t v1.0.0

# Build and push to registry
./docker/scripts/build.sh -t my-registry/ear-trainer -p

# Build for development
./docker/scripts/build.sh -e dev
```

### deploy.sh
Deploy the application using Docker Compose.

```bash
# Start development environment
./docker/scripts/deploy.sh -e dev -a up

# Start production environment
./docker/scripts/deploy.sh -e prod -a up

# Stop services
./docker/scripts/deploy.sh -a down

# View logs
./docker/scripts/deploy.sh -a logs

# Restart services
./docker/scripts/deploy.sh -a restart
```

### cleanup.sh
Clean up Docker resources.

```bash
# Basic cleanup (containers and volumes)
./docker/scripts/cleanup.sh

# Clean up everything including images
./docker/scripts/cleanup.sh -a

# Force cleanup without confirmation
./docker/scripts/cleanup.sh -f
```

## Environment Configurations

### Development (docker-compose.dev.yml)
- Hot reload enabled for backend
- Frontend served by development server
- Debug mode enabled
- No SSL/HTTPS
- Simplified nginx configuration

### Production (docker-compose.prod.yml)
- Optimized for performance
- SSL/HTTPS support
- Redis for caching
- Comprehensive nginx configuration
- Health checks enabled

## Nginx Configurations

### Development (nginx.dev.conf)
- Simple proxy configuration
- Frontend served by React dev server
- No SSL/HTTPS
- Basic logging

### Production (nginx.prod.conf)
- SSL/HTTPS termination
- Static file serving
- Rate limiting
- Security headers
- Gzip compression
- Comprehensive logging

## Environment Variables

### Required for Production
```bash
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=your-domain.com
DB_NAME=open_ear_trainer
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
```

### Optional
```bash
REDIS_URL=redis://redis:6379/1
AUDIO_CACHE_ENABLED=True
AUDIO_CACHE_MAX_SIZE=1000
```

## Troubleshooting

### Common Issues

1. **Port conflicts**: Make sure ports 80, 443, 3000, 8000, and 6379 are available
2. **Permission issues**: Ensure Docker has proper permissions
3. **Build failures**: Check that all dependencies are properly installed
4. **SSL issues**: Ensure SSL certificates are properly configured for production

### Logs
```bash
# View all logs
docker-compose -f docker/docker-compose.prod.yml logs

# View specific service logs
docker-compose -f docker/docker-compose.prod.yml logs web
docker-compose -f docker/docker-compose.prod.yml logs nginx
```

### Health Checks
```bash
# Check service health
docker-compose -f docker/docker-compose.prod.yml ps

# Test API endpoint
curl http://localhost/api/exercises/

# Test frontend
curl http://localhost/
```

## Integration with Main Deployment Script

The main deployment script (`deploy.py`) automatically uses these Docker configurations:

```bash
# Deploy to development
python deploy.py docker --env dev

# Deploy to production
python deploy.py docker --env prod

# Full deployment with custom tag
python deploy.py full --tag v1.0.0 --env prod
```
