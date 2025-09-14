#!/usr/bin/env python3
"""
Restart the main server with fixes
"""
import subprocess
import sys
import os
import time

def restart_main_server():
    """Restart the main server"""
    print("🔄 Restarting main server...")
    
    # Kill existing processes
    try:
        os.system("pkill -f start_server.py")
        os.system("pkill -f uvicorn")
        os.system("pkill -f minimal_test_server.py")
        time.sleep(2)
        print("✅ Killed existing processes")
    except:
        pass
    
    # Start main server
    try:
        print("🚀 Starting main server...")
        process = subprocess.Popen([sys.executable, 'start_server.py'])
        print(f"✅ Main server started with PID: {process.pid}")
        print("📍 Server available at: http://localhost:8000")
        print("⏳ Wait 5 seconds then test upload...")
        return True
    except Exception as e:
        print(f"❌ Failed to start: {e}")
        return False

if __name__ == "__main__":
    restart_main_server()