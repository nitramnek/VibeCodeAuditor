#!/usr/bin/env python3
"""
Restart the VibeCodeAuditor server
"""
import subprocess
import sys
import os
import signal
import time
from pathlib import Path

def kill_existing_servers():
    """Kill any existing server processes"""
    try:
        # Try to find and kill existing python processes on port 8000
        result = subprocess.run(['lsof', '-ti:8000'], capture_output=True, text=True)
        if result.stdout.strip():
            pids = result.stdout.strip().split('\n')
            for pid in pids:
                try:
                    os.kill(int(pid), signal.SIGTERM)
                    print(f"Killed process {pid}")
                except:
                    pass
        time.sleep(2)
    except:
        pass

def start_server():
    """Start the server"""
    try:
        print("🚀 Starting VibeCodeAuditor server...")
        
        # Add current directory to Python path
        current_dir = Path(__file__).parent
        env = os.environ.copy()
        env['PYTHONPATH'] = str(current_dir)
        
        # Start the server
        process = subprocess.Popen([
            sys.executable, 'start_server.py'
        ], env=env)
        
        print(f"✅ Server started with PID: {process.pid}")
        print("📍 Server should be available at: http://localhost:8000")
        print("📚 Health check: http://localhost:8000/health")
        
        return process
        
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        return None

if __name__ == "__main__":
    print("🔄 Restarting VibeCodeAuditor Server")
    print("=" * 40)
    
    # Kill existing servers
    kill_existing_servers()
    
    # Start new server
    process = start_server()
    
    if process:
        try:
            # Wait a bit for server to start
            time.sleep(3)
            
            # Test health endpoint
            try:
                import requests
                response = requests.get("http://localhost:8000/health", timeout=5)
                if response.status_code == 200:
                    print("✅ Server is healthy!")
                    print(f"Response: {response.json()}")
                else:
                    print(f"⚠️ Server responded with status: {response.status_code}")
            except Exception as e:
                print(f"⚠️ Could not test health endpoint: {e}")
            
            print("\n🎉 Server restart complete!")
            print("Press Ctrl+C to stop the server")
            
            # Keep the script running
            process.wait()
            
        except KeyboardInterrupt:
            print("\n🛑 Stopping server...")
            process.terminate()
            process.wait()
            print("✅ Server stopped")
    else:
        sys.exit(1)