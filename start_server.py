#!/usr/bin/env python3
"""
Simple server startup script for VibeCodeAuditor.
"""

import sys
import os
from pathlib import Path

def main():
    print("🚀 VibeCodeAuditor Server Startup")
    print("=" * 40)
    
    # Add current directory to Python path
    current_dir = Path(__file__).parent
    sys.path.insert(0, str(current_dir))
    
    try:
        # Test imports first
        print("🧪 Testing imports...")
        from vibeauditor.main import app
        print("✅ All imports successful")
        
        # Start server with uvicorn directly
        print("🌐 Starting server on http://localhost:8000")
        print("📚 API docs will be available at http://localhost:8000/api/docs")
        print("🔧 Press Ctrl+C to stop")
        print()
        
        import uvicorn
        uvicorn.run(
            app,
            host="127.0.0.1",
            port=8000,
            reload=False,  # Set to True for development
            log_level="info"
        )
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure you've installed dependencies: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Server startup failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()