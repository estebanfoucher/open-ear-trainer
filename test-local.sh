#!/bin/bash

# Test with local backend
echo "🚀 Starting local backend and frontend..."

# Kill any existing processes
pkill -f "react-scripts start" 2>/dev/null
pkill -f "python manage.py runserver" 2>/dev/null

# Start backend in background
echo "📡 Starting Django backend on port 8000..."
cd backend && source ../.venv/bin/activate && DJANGO_SETTINGS_MODULE=config.settings.development python manage.py runserver 8000 &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

# Start frontend
echo "🌐 Starting React frontend on port 3000..."
cd ../frontend && REACT_APP_API_URL=http://localhost:8000 npm start &
FRONTEND_PID=$!

echo ""
echo "✅ Local testing environment started!"
echo "   Backend:  http://localhost:8000"
echo "   Frontend: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop both services"

# Wait for user to stop
wait

# Cleanup
echo "🛑 Stopping services..."
kill $BACKEND_PID 2>/dev/null
kill $FRONTEND_PID 2>/dev/null
echo "✅ Services stopped"
