# Local Testing Guide

This guide helps you test your Open Ear Trainer application locally with different backend configurations.

## 🚀 Quick Start

### Test with Local Backend
```bash
./test-local.sh
```
- Starts Django backend on `http://localhost:8000`
- Starts React frontend on `http://localhost:3000`
- Frontend connects to local backend
- Press `Ctrl+C` to stop both services

### Test with Railway Backend
```bash
./test-railway.sh
```
- Starts React frontend on `http://localhost:3000`
- Frontend connects to Railway backend at `https://open-ear-trainer-production.up.railway.app`
- Press `Ctrl+C` to stop

## 🔧 Manual Testing

### Backend Only
```bash
cd backend
source ../.venv/bin/activate
DJANGO_SETTINGS_MODULE=config.settings.development python manage.py runserver 8000
```

### Frontend Only (Local Backend)
```bash
cd frontend
REACT_APP_API_URL=http://localhost:8000 npm start
```

### Frontend Only (Railway Backend)
```bash
cd frontend
REACT_APP_API_URL=https://open-ear-trainer-production.up.railway.app npm start
```

## 🧪 Testing Checklist

### Local Backend Test
- [ ] Backend starts without errors
- [ ] API accessible at `http://localhost:8000/api/`
- [ ] Health endpoint works at `http://localhost:8000/health/`
- [ ] Frontend loads at `http://localhost:3000`
- [ ] Exercises load in frontend
- [ ] No CORS errors in browser console

### Railway Backend Test
- [ ] Frontend loads at `http://localhost:3000`
- [ ] Exercises load from Railway backend
- [ ] No CORS errors in browser console
- [ ] API calls go to `https://open-ear-trainer-production.up.railway.app`

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Kill processes on ports 3000 and 8000
lsof -ti:3000 | xargs kill -9
lsof -ti:8000 | xargs kill -9
```

### Backend Won't Start
- Check if virtual environment is activated
- Ensure all dependencies are installed: `uv pip install -e ".[dev]"`
- Check Django settings: `DJANGO_SETTINGS_MODULE=config.settings.development`

### Frontend Won't Connect to Backend
- Check browser console for CORS errors
- Verify `REACT_APP_API_URL` is set correctly
- Test backend API directly: `curl http://localhost:8000/api/exercises/`

### Railway Backend Issues
- Test Railway API: `curl https://open-ear-trainer-production.up.railway.app/api/exercises/`
- Check Railway deployment logs
- Verify CORS settings in production.py

## 📝 Environment Variables

### Frontend
- `REACT_APP_API_URL`: Backend API URL
  - Local: `http://localhost:8000`
  - Railway: `https://open-ear-trainer-production.up.railway.app`

### Backend
- `DJANGO_SETTINGS_MODULE`: Django settings module
  - Development: `config.settings.development`
  - Production: `config.settings.production`

## 🎯 Expected Behavior

### Local Setup
- Backend serves API at `http://localhost:8000`
- Frontend serves UI at `http://localhost:3000`
- Frontend makes API calls to local backend
- All CORS issues resolved

### Railway Setup
- Railway serves API at `https://open-ear-trainer-production.up.railway.app`
- Frontend serves UI at `http://localhost:3000`
- Frontend makes API calls to Railway backend
- CORS allows localhost requests

### GitHub Pages Setup
- Railway serves API at `https://open-ear-trainer-production.up.railway.app`
- GitHub Pages serves UI at `https://estebanfoucher.github.io/open-ear-trainer`
- Frontend makes API calls to Railway backend
- CORS allows GitHub Pages requests
