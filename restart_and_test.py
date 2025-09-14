#!/usr/bin/env python3
"""
Restart server and test upload
"""
import subprocess
import time
import os
import sys

def restart_and_test():
    """Restart server and test"""
    print("🔄 Restarting server with updated patterns...")
    
    # Kill existing processes
    os.system("pkill -f start_server.py")
    os.system("pkill -f uvicorn")
    time.sleep(2)
    
    # Start server
    print("🚀 Starting server...")
    process = subprocess.Popen([sys.executable, 'start_server.py'])
    
    print("✅ Server started")
    print("📍 Available at: http://localhost:8000")
    print("🧪 Now test uploading test_security_issues.js in your browser")
    print("💡 The updated patterns should detect:")
    print("   - Hardcoded passwords (PASSWORD, password)")
    print("   - API keys (API_KEY, apiKey)")
    print("   - Secrets (SECRET)")
    print("   - eval() usage")
    print("   - innerHTML XSS risks")
    print("   - Database connection strings")
    print("   - AWS access keys")
    print()
    print("⏳ Server is running... Press Ctrl+C to stop")
    
    try:
        process.wait()
    except KeyboardInterrupt:
        print("\\n🛑 Stopping server...")
        process.terminate()

if __name__ == "__main__":
    restart_and_test()