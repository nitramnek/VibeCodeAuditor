#!/usr/bin/env python3
"""
Development server launcher for VibeCodeAuditor PWA.
"""

import sys
import subprocess
from pathlib import Path

def main():
    """Launch the development server."""
    
    print("🚀 Starting VibeCodeAuditor PWA Development Server")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("vibeauditor").exists():
        print("❌ Error: Please run this script from the project root directory")
        sys.exit(1)
    
    # Install dependencies if needed
    try:
        import fastapi
        import uvicorn
    except ImportError:
        print("📦 Installing required dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
    
    # Start the server
    try:
        print("🌐 Starting API server on http://localhost:8000")
        print("📚 API docs available at http://localhost:8000/api/docs")
        print("🔧 Press Ctrl+C to stop the server")
        print()
        
        import uvicorn
        from vibeauditor.api.main import app
        
        uvicorn.run(
            app,
            host="127.0.0.1",
            port=8000,
            reload=True,
            log_level="info"
        )
        
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()