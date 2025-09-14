#!/usr/bin/env python3
"""
Test the mock server to verify frontend integration
"""
import subprocess
import time
import requests
import sys
import os
import signal

def start_mock_server():
    """Start the mock server"""
    try:
        print("🚀 Starting mock server...")
        
        # Start mock server
        process = subprocess.Popen([
            sys.executable, 'mock_api_server.py'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print(f"✅ Mock server started with PID: {process.pid}")
        
        # Wait for server to start
        time.sleep(3)
        
        return process
        
    except Exception as e:
        print(f"❌ Failed to start mock server: {e}")
        return None

def test_mock_server():
    """Test the mock server endpoints"""
    try:
        print("🧪 Testing mock server...")
        
        # Test health endpoint
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health endpoint working!")
            data = response.json()
            print(f"   Status: {data.get('status')}")
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
            return False
        
        # Test upload endpoint
        files = {'file': ('test.py', 'print("hello")', 'text/plain')}
        data = {'user_id': 'test-user-123'}
        
        response = requests.post(
            "http://localhost:8000/scan",
            files=files,
            data=data,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Upload endpoint working!")
            result = response.json()
            print(f"   Scan ID: {result.get('scan_id')}")
            print(f"   Status: {result.get('status')}")
            
            # Test get results
            scan_id = result.get('scan_id')
            if scan_id:
                response = requests.get(f"http://localhost:8000/scan/{scan_id}")
                if response.status_code == 200:
                    print("✅ Get results endpoint working!")
                    results = response.json()
                    print(f"   Issues found: {len(results.get('issues', []))}")
                    return True
        
        print(f"❌ Upload test failed: {response.status_code}")
        return False
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Mock Server Integration")
    print("=" * 40)
    
    # Start mock server
    process = start_mock_server()
    
    if process:
        try:
            # Test the server
            success = test_mock_server()
            
            if success:
                print("\n🎉 Mock server tests passed!")
                print("✅ Frontend integration should work")
                print("💡 The mock server is now running on http://localhost:8000")
                print("💡 Try uploading a file in the web interface")
                print("💡 Press Ctrl+C to stop the mock server")
                
                # Keep server running
                try:
                    process.wait()
                except KeyboardInterrupt:
                    print("\n🛑 Stopping mock server...")
                    process.terminate()
                    process.wait()
                    print("✅ Mock server stopped")
            else:
                print("\n❌ Mock server tests failed")
                process.terminate()
                
        except Exception as e:
            print(f"❌ Error: {e}")
            process.terminate()
    else:
        print("❌ Could not start mock server")
        sys.exit(1)