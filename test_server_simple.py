#!/usr/bin/env python3
"""
Simple test to start the server
"""
import sys
import os
from pathlib import Path

# Add current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

print("Testing server startup...")

try:
    from vibeauditor.main import app
    print("✅ App imported successfully")
    
    import uvicorn
    print("✅ Uvicorn imported successfully")
    
    print("🚀 Starting server...")
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()