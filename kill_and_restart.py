#!/usr/bin/env python3
"""
Kill existing server and restart with new code
"""
import subprocess
import sys
import os
import time
import signal

def kill_existing_servers():
    """Kill any existing server processes"""
    try:
        print("🔍 Looking for existing server processes...")
        
        # Method 1: Kill by port
        try:
            result = subprocess.run(['lsof', '-ti:8000'], capture_output=True, text=True)
            if result.stdout.strip():
                pids = result.stdout.strip().split('\n')
                for pid in pids:
                    try:
                        os.kill(int(pid), signal.SIGTERM)
                        print(f"✅ Killed process {pid} on port 8000")
                    except:
                        pass
        except:
            pass
        
        # Method 2: Kill by process name
        try:
            result = subprocess.run(['pgrep', '-f', 'start_server.py'], capture_output=True, text=True)
            if result.stdout.strip():
                pids = result.stdout.strip().split('\n')
                for pid in pids:
                    try:
                        os.kill(int(pid), signal.SIGTERM)
                        print(f"✅ Killed start_server.py process {pid}")
                    except:
                        pass
        except:
            pass
        
        # Method 3: Kill uvicorn processes
        try:
            result = subprocess.run(['pgrep', '-f', 'uvicorn'], capture_output=True, text=True)
            if result.stdout.strip():
                pids = result.stdout.strip().split('\n')
                for pid in pids:
                    try:
                        os.kill(int(pid), signal.SIGTERM)
                        print(f"✅ Killed uvicorn process {pid}")
                    except:
                        pass
        except:
            pass
            
        print("⏳ Waiting for processes to terminate...")
        time.sleep(3)
        
    except Exception as e:
        print(f"⚠️ Error killing processes: {e}")

def start_server():
    """Start the server"""
    try:
        print("🚀 Starting fresh server...")
        
        # Start server in background
        process = subprocess.Popen([
            sys.executable, 'start_server.py'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print(f"✅ Server started with PID: {process.pid}")
        print("📍 Server should be available at: http://localhost:8000")
        
        # Wait a moment for server to start
        time.sleep(5)
        
        # Test if server is responding
        try:
            import requests
            response = requests.get("http://localhost:8000/health", timeout=5)
            if response.status_code == 200:
                print("✅ Server is healthy and responding!")
                data = response.json()
                print(f"   Status: {data.get('status')}")
                print(f"   Environment: {data.get('environment')}")
                return True
            else:
                print(f"⚠️ Server responded with status: {response.status_code}")
                return False
        except Exception as e:
            print(f"⚠️ Could not test server health: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        return False

if __name__ == "__main__":
    print("🔄 Restarting VibeCodeAuditor Server")
    print("=" * 40)
    
    # Kill existing servers
    kill_existing_servers()
    
    # Start new server
    success = start_server()
    
    if success:
        print("\n🎉 Server restart successful!")
        print("✅ Ready to test frontend integration")
        print("💡 Try uploading a file in the web interface")
    else:
        print("\n❌ Server restart failed")
        print("💡 Check logs/vibeauditor.log for details")
        
        # Show recent logs
        try:
            with open('logs/vibeauditor.log', 'r') as f:
                lines = f.readlines()
                print("\n📋 Recent log entries:")
                for line in lines[-5:]:
                    print(f"   {line.strip()}")
        except:
            pass