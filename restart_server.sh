#!/bin/bash
echo "🔄 Restarting server with updated patterns..."

# Kill existing processes
pkill -f "start_server.py" 2>/dev/null
pkill -f "uvicorn" 2>/dev/null
sleep 2

# Start server
echo "🚀 Starting server..."
source venv/bin/activate && python start_server.py &

echo "✅ Server restarted"
echo "📍 Available at: http://localhost:8000"
echo "🧪 Upload test.js again - should now find 6+ security issues!"