#!/usr/bin/env python3
"""Test if the VibeCodeAuditor server is running."""

import requests
import json

def test_server():
    print("🧪 Testing VibeCodeAuditor Server")
    print("=" * 40)
    
    try:
        # Test health endpoint
        print("🔍 Testing health endpoint...")
        response = requests.get("http://localhost:8000/health", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Server is running!")
            print(f"   Status: {data.get('status')}")
            print(f"   Environment: {data.get('environment')}")
            print(f"   Version: {data.get('version')}")
            print(f"   Scanners: {data.get('scanners_available')}")
            
            # Test API docs
            print("\n🔍 Testing API documentation...")
            docs_response = requests.get("http://localhost:8000/docs", timeout=5)
            if docs_response.status_code == 200:
                print("✅ API documentation available at http://localhost:8000/docs")
            
            print("\n🎉 VibeCodeAuditor is fully operational!")
            print("🌐 Server: http://localhost:8000")
            print("📚 API Docs: http://localhost:8000/docs")
            print("🔍 Health: http://localhost:8000/health")
            
            return True
        else:
            print(f"❌ Server responded with status {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server")
        print("💡 Make sure the server is running: python start_server.py")
        return False
    except Exception as e:
        print(f"❌ Error testing server: {e}")
        return False

if __name__ == "__main__":
    test_server()