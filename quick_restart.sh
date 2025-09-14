#!/bin/bash
echo "🔄 Quick restart..."

# Kill existing processes
pkill -f "start_server.py" 2>/dev/null
pkill -f "uvicorn" 2>/dev/null
sleep 2

# Start server in background
echo "🚀 Starting server..."
source venv/bin/activate && python start_server.py &

echo "✅ Server started"
echo "📍 Available at: http://localhost:8000"
echo "⏳ Wait 3 seconds then test upload..."