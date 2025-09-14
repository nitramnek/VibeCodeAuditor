#!/bin/bash

echo "🚀 VibeCodeAuditor Quick Start"
echo "=============================="

# Check if we're in the right directory
if [ ! -f "vibeauditor/__init__.py" ]; then
    echo "❌ Please run this script from the VibeCodeAuditor project root directory"
    exit 1
fi

echo "📍 Current directory: $(pwd)"
echo "✅ Project structure looks good"

# Function to check if a port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# Check if API server is running
if check_port 8000; then
    echo "✅ API server is already running on port 8000"
else
    echo "🚀 Starting API server..."
    echo "   Run this in a separate terminal: python start_server.py"
    echo "   Or press Ctrl+C and run: python start_server.py &"
fi

# Check if webapp directory exists
if [ ! -d "webapp" ]; then
    echo "❌ webapp directory not found"
    exit 1
fi

echo "📁 Webapp directory found"

# Navigate to webapp and check setup
cd webapp

if [ ! -f "package.json" ]; then
    echo "❌ package.json not found in webapp directory"
    exit 1
fi

echo "✅ package.json found"

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing webapp dependencies..."
    npm install
    
    if [ $? -ne 0 ]; then
        echo "❌ npm install failed"
        echo "💡 Try running manually:"
        echo "   cd webapp"
        echo "   rm -rf node_modules package-lock.json"
        echo "   npm install"
        exit 1
    fi
else
    echo "✅ Dependencies already installed"
fi

echo ""
echo "🎉 Setup complete! Now run:"
echo ""
echo "Terminal 1 (API Server):"
echo "  python start_server.py"
echo ""
echo "Terminal 2 (Web App):"
echo "  cd webapp"
echo "  npm start"
echo ""
echo "Then open http://localhost:3000 in your browser!"
echo ""
echo "📚 For detailed instructions, see START_HERE.md"