#!/bin/bash

# Test with Railway backend
echo "🚀 Starting frontend with Railway backend..."

# Kill any existing processes
pkill -f "react-scripts start" 2>/dev/null

# Start frontend with Railway backend
echo "🌐 Starting React frontend on port 3000..."
echo "   Backend: https://open-ear-trainer-production.up.railway.app"
cd frontend && REACT_APP_API_URL=https://open-ear-trainer-production.up.railway.app npm start &
FRONTEND_PID=$!

echo ""
echo "✅ Frontend started with Railway backend!"
echo "   Frontend: http://localhost:3000"
echo "   Backend:  https://open-ear-trainer-production.up.railway.app"
echo ""
echo "Press Ctrl+C to stop"

# Wait for user to stop
wait

# Cleanup
echo "🛑 Stopping frontend..."
kill $FRONTEND_PID 2>/dev/null
echo "✅ Frontend stopped"
