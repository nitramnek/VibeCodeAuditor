#!/usr/bin/env python3
"""
Test server health and basic functionality
"""
import requests
import json
import time

def test_health():
    """Test the health endpoint"""
    try:
        print("🧪 Testing health endpoint...")
        response = requests.get("http://localhost:8000/health", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Health endpoint working!")
            print(f"   Status: {data.get('status')}")
            print(f"   Environment: {data.get('environment')}")
            print(f"   Version: {data.get('version')}")
            return True
        else:
            print(f"❌ Health endpoint failed with status: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Is it running?")
        return False
    except Exception as e:
        print(f"❌ Health test failed: {e}")
        return False

def test_upload_endpoint():
    """Test the upload endpoint structure (without actually uploading)"""
    try:
        print("\n🧪 Testing upload endpoint structure...")
        
        # Create a simple test file
        files = {'file': ('test.py', 'print("hello world")', 'text/plain')}
        data = {'user_id': 'test-user-123'}
        
        response = requests.post(
            "http://localhost:8000/scan",
            files=files,
            data=data,
            timeout=10
        )
        
        print(f"   Response status: {response.status_code}")
        
        if response.status_code == 401:
            print("✅ Upload endpoint exists (authentication required)")
            return True
        elif response.status_code == 200:
            print("✅ Upload endpoint working!")
            try:
                data = response.json()
                print(f"   Response: {data}")
            except:
                pass
            return True
        else:
            print(f"⚠️ Upload endpoint responded with: {response.status_code}")
            try:
                print(f"   Response: {response.text}")
            except:
                pass
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server for upload test")
        return False
    except Exception as e:
        print(f"❌ Upload test failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing VibeCodeAuditor Server")
    print("=" * 40)
    
    # Test health
    health_ok = test_health()
    
    if health_ok:
        # Test upload endpoint
        upload_ok = test_upload_endpoint()
        
        if health_ok and upload_ok:
            print("\n🎉 Server tests passed!")
            print("✅ Ready for frontend integration")
        else:
            print("\n⚠️ Some tests failed, but server is responding")
    else:
        print("\n❌ Server is not responding")
        print("💡 Try starting the server with: python start_server.py")