# Deployment Guide

This guide covers deploying the Open Ear Trainer application using various methods and the included CLI deployment script.

## Prerequisites

Before deploying, ensure you have the following tools installed:

- **Git** - Version control
- **Docker** & **Docker Compose** - Containerization
- **Node.js 18+** - Frontend build
- **Python 3.11+** - Backend runtime
- **uv** - Python package management

## Quick Start with CLI

The easiest way to deploy is using the included CLI script:

```bash
# Make the script executable (if not already)
chmod +x deploy.py

# Deploy everything with Docker
python deploy.py full

# Deploy only frontend to GitHub Pages
python deploy.py github-pages

# Deploy only backend to Railway
python deploy.py railway

# Run tests only
python deploy.py test

# Build without deploying
python deploy.py build
```

## Deployment Options

### 1. Docker Deployment (Recommended for VPS/Cloud)

Deploy using Docker containers with Nginx reverse proxy:

```bash
# Full deployment with tests and linting
python deploy.py docker

# Skip tests and linting for faster deployment
python deploy.py docker --skip-tests --skip-lint

# Use custom Docker tag
python deploy.py docker --tag my-ear-trainer
```

**What this does:**
- Builds React frontend for production
- Creates Docker image with Django backend
- Sets up Nginx reverse proxy
- Configures static file serving
- Enables audio file caching

### 2. GitHub Pages (Frontend Only)

Deploy the React frontend to GitHub Pages:

```bash
python deploy.py github-pages
```

**Setup required:**
1. Enable GitHub Pages in repository settings
2. Set `CUSTOM_DOMAIN` secret in GitHub repository settings
3. Configure `REACT_APP_API_URL` environment variable

### 3. Railway (Backend Only)

Deploy Django backend to Railway:

```bash
python deploy.py railway
```

**Setup required:**
1. Install Railway CLI: `npm install -g @railway/cli`
2. Login: `railway login`
3. Create new project: `railway init`
4. Set environment variables in Railway dashboard

### 4. Full Stack Deployment

For complete deployment with both frontend and backend:

```bash
python deploy.py full
```

## Environment Configuration

### Required Environment Variables

Copy `env.example` to `.env` and configure:

```bash
cp env.example .env
```

**Essential variables:**
- `SECRET_KEY` - Django secret key (generate with `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
- `ALLOWED_HOSTS` - Comma-separated list of allowed domains
- `CORS_ALLOWED_ORIGINS` - Frontend domains for CORS
- `REACT_APP_API_URL` - Backend API URL for frontend

**Database (for production):**
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`

**Optional:**
- `REDIS_URL` - For caching and sessions
- `EMAIL_*` - For email functionality
- `AUDIO_CACHE_*` - Audio file caching settings

### GitHub Secrets

For GitHub Actions deployment, set these repository secrets:

- `REACT_APP_API_URL` - Backend API URL
- `CUSTOM_DOMAIN` - Custom domain for GitHub Pages
- `RAILWAY_TOKEN` - Railway deployment token
- `RAILWAY_PROJECT_ID` - Railway project ID

## Manual Deployment Steps

### Docker Deployment

1. **Build and run:**
   ```bash
   docker-compose up -d
   ```

2. **Check status:**
   ```bash
   docker-compose ps
   docker-compose logs -f
   ```

3. **Update deployment:**
   ```bash
   docker-compose down
   docker-compose up -d --build
   ```

### Frontend Build

1. **Install dependencies:**
   ```bash
   cd frontend
   npm ci
   ```

2. **Build for production:**
   ```bash
   npm run build
   ```

3. **Serve static files:**
   ```bash
   # Using serve (install with: npm install -g serve)
   serve -s build -l 3000
   ```

### Backend Deployment

1. **Install dependencies:**
   ```bash
   uv venv
   source .venv/bin/activate
   uv pip install -e ".[dev]"
   ```

2. **Run migrations:**
   ```bash
   cd backend
   python manage.py migrate
   ```

3. **Collect static files:**
   ```bash
   python manage.py collectstatic --noinput
   ```

4. **Start server:**
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

## Production Considerations

### Security

- Use strong `SECRET_KEY`
- Set `DEBUG=False`
- Configure proper `ALLOWED_HOSTS`
- Enable HTTPS with SSL certificates
- Use environment variables for sensitive data

### Performance

- Enable Redis caching
- Configure CDN for static files
- Use database connection pooling
- Monitor audio file generation

### Monitoring

- Set up logging
- Monitor disk space (audio files)
- Track API response times
- Monitor error rates

## Troubleshooting

### Common Issues

1. **Docker build fails:**
   - Check Docker is running
   - Ensure sufficient disk space
   - Verify Dockerfile syntax

2. **Frontend build fails:**
   - Check Node.js version (18+)
   - Clear npm cache: `npm cache clean --force`
   - Delete node_modules and reinstall

3. **Backend deployment fails:**
   - Check Python version (3.11+)
   - Verify environment variables
   - Check database connectivity

4. **Audio generation fails:**
   - Verify SoundFont file exists
   - Check FluidSynth installation
   - Ensure write permissions for media directory

### Logs

- **Docker logs:** `docker-compose logs -f`
- **Django logs:** Check `logs/django.log`
- **Nginx logs:** `docker-compose logs nginx`

### Health Checks

- **API health:** `curl http://localhost:8000/api/exercises/`
- **Frontend:** `curl http://localhost/`
- **Docker health:** `docker-compose ps`

## Scaling

### Horizontal Scaling

- Use load balancer (Nginx, HAProxy)
- Deploy multiple backend instances
- Use Redis for session storage
- Configure database replication

### Vertical Scaling

- Increase server resources
- Optimize database queries
- Enable audio file caching
- Use CDN for static assets

## Backup Strategy

1. **Database backups:**
   ```bash
   python manage.py dumpdata > backup.json
   ```

2. **Media files:**
   ```bash
   tar -czf media-backup.tar.gz media/
   ```

3. **Automated backups:**
   - Set up cron jobs
   - Use cloud storage (S3, GCS)
   - Implement retention policies

## Support

For deployment issues:

1. Check this documentation
2. Review logs for errors
3. Test with development setup
4. Create GitHub issue with details

## Next Steps

After successful deployment:

1. Set up monitoring and alerting
2. Configure automated backups
3. Implement CI/CD pipeline
4. Set up staging environment
5. Plan for scaling and optimization
