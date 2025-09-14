#!/usr/bin/env python3
"""
Simple test to verify the mock API server works
"""

import subprocess
import sys
import time
import os

def main():
    print("🧪 Simple Backend Test")
    print("=" * 30)
    
    # Check if mock_api_server.py exists
    if not os.path.exists("mock_api_server.py"):
        print("❌ mock_api_server.py not found")
        return
    
    print("✅ Found mock_api_server.py")
    
    # Try to import required modules
    try:
        import fastapi
        import uvicorn
        print("✅ FastAPI and uvicorn are available")
    except ImportError as e:
        print(f"❌ Missing dependencies: {e}")
        print("Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "fastapi", "uvicorn"])
    
    # Start the server
    print("🚀 Starting mock server...")
    try:
        process = subprocess.Popen([
            sys.executable, "mock_api_server.py"
        ])
        
        print("✅ Server process started")
        print("🌐 Server should be available at: http://localhost:8000")
        print("📚 Health check: http://localhost:8000/health")
        print("📤 Upload endpoint: http://localhost:8000/scan")
        print()
        print("🎯 Next steps:")
        print("1. Open your browser to http://localhost:3000 (React app)")
        print("2. Upload a test file")
        print("3. Check if issues are displayed correctly")
        print()
        print("Press Ctrl+C to stop the server")
        
        # Wait for user to stop
        process.wait()
        
    except KeyboardInterrupt:
        print("\n👋 Stopping server...")
        process.terminate()
        process.wait()
        print("✅ Server stopped")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()