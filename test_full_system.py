#!/usr/bin/env python3
"""
Comprehensive system test for VibeCodeAuditor
"""
import subprocess
import time
import requests
import sys
import os

def test_full_system():
    """Test the complete system end-to-end"""
    print("🧪 Comprehensive VibeCodeAuditor System Test")
    print("=" * 50)
    
    # Kill existing servers
    print("🔧 Cleaning up existing processes...")
    os.system("pkill -f start_server.py")
    os.system("pkill -f uvicorn")
    time.sleep(2)
    
    # Start main server
    print("🚀 Starting main server...")
    process = subprocess.Popen([sys.executable, 'start_server.py'])
    
    # Wait for server to start
    print("⏳ Waiting for server to initialize...")
    time.sleep(5)
    
    try:
        # Test health endpoint
        print("\\n🧪 Testing health endpoint...")
        response = requests.get("http://localhost:8000/health", timeout=10)
        
        if response.status_code != 200:
            print(f"❌ Health failed: {response.status_code}")
            return False
            
        print("✅ Health endpoint working!")
        
        # Test upload with vulnerable file
        print("\\n🧪 Testing upload with vulnerable file...")
        
        vulnerable_content = '''#!/usr/bin/env python3
API_KEY = "sk-1234567890abcdef"
PASSWORD = "admin123"

def vulnerable_function():
    user_input = input("Enter user ID: ")
    query = f"SELECT * FROM users WHERE id = {user_input}"
    eval(user_input)
    return query
'''
        
        files = {'file': ('vulnerable_test.py', vulnerable_content, 'text/plain')}
        data = {'user_id': '289c36cf-8779-4e49-bcfe-b829d0899472'}
        
        response = requests.post("http://localhost:8000/scan", files=files, data=data, timeout=15)
        
        if response.status_code != 200:
            print(f"❌ Upload failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
        print("✅ Upload successful!")
        result = response.json()
        scan_id = result.get('scan_id')
        print(f"Scan ID: {scan_id}")
        
        if not scan_id:
            print("❌ No scan ID returned")
            return False
            
        # Wait for scan to complete
        print("\\n⏳ Waiting for scan to complete...")
        time.sleep(8)
        
        # Get results
        print("🧪 Getting scan results...")
        response = requests.get(f"http://localhost:8000/scan/{scan_id}", timeout=10)
        
        if response.status_code != 200:
            print(f"❌ Failed to get results: {response.status_code}")
            return False
            
        print("✅ Results retrieved successfully!")
        results = response.json()
        
        issues = results.get('issues', [])
        print(f"Issues Found: {len(issues)}")
        
        if issues:
            print("\\n🔍 Security Issues Detected:")
            for i, issue in enumerate(issues[:3], 1):
                print(f"{i}. {issue.get('severity')} - {issue.get('description')}")
        
        return len(issues) > 0
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
    finally:
        process.terminate()

if __name__ == "__main__":
    success = test_full_system()
    if success:
        print("\\n🎉 SYSTEM TEST PASSED!")
    else:
        print("\\n❌ SYSTEM TEST FAILED")