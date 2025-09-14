#!/bin/bash

echo "🚀 Setting up VibeCodeAuditor Web App"
echo "===================================="

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first:"
    echo "   https://nodejs.org/"
    exit 1
fi

echo "✅ Node.js version: $(node --version)"

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm first."
    exit 1
fi

echo "✅ npm version: $(npm --version)"

# Navigate to webapp directory
cd webapp

echo "📦 Cleaning up old dependencies..."
rm -rf node_modules package-lock.json

echo "📦 Installing dependencies..."
npm install

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully!"
    echo ""
    echo "🌐 To start the development server:"
    echo "   cd webapp"
    echo "   npm start"
    echo ""
    echo "📚 The app will be available at http://localhost:3000"
    echo "🔗 Make sure your API server is running on http://localhost:8000"
else
    echo "❌ Failed to install dependencies"
    echo "💡 Try running manually:"
    echo "   cd webapp"
    echo "   rm -rf node_modules package-lock.json"
    echo "   npm install"
    exit 1
fi