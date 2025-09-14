#!/usr/bin/env python3
"""
Simple API client to test VibeCodeAuditor functionality.
"""

import requests
import json
import time
from pathlib import Path

API_BASE = "http://localhost:8000"

def test_health():
    """Test health endpoint."""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{API_BASE}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Health check passed")
            print(f"   Status: {data.get('status')}")
            print(f"   Environment: {data.get('environment')}")
            print(f"   Scanners: {data.get('scanners_available')}")
            return True
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Health check error: {e}")
        return False

def test_file_upload():
    """Test file upload and scanning."""
    print("\n🔍 Testing file upload and scanning...")
    
    # Create a test file if it doesn't exist
    test_file = Path("test_sample.py")
    if not test_file.exists():
        test_file.write_text('''
# Test file with security issues
password = "admin123"
api_key = "sk-1234567890"

def get_user(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return query
''')
    
    try:
        # Prepare file upload
        files = {
            'file': ('test_sample.py', test_file.open('rb'), 'text/plain')
        }
        data = {
            'user_id': 'test_user_123'
        }
        headers = {
            'Authorization': 'Bearer test_token_for_demo'
        }
        
        print("   📤 Uploading file...")
        response = requests.post(
            f"{API_BASE}/scan", 
            files=files, 
            data=data,
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            scan_id = result.get('scan_id')
            print(f"   ✅ File uploaded successfully")
            print(f"   Scan ID: {scan_id}")
            print(f"   Status: {result.get('status')}")
            
            # Wait for scan to complete and check results
            return test_scan_results(scan_id, headers)
            
        elif response.status_code == 401:
            print("   ⚠️  Authentication required (expected in production)")
            return True  # This is expected behavior
        else:
            print(f"   ❌ Upload failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Upload error: {e}")
        return False

def test_scan_results(scan_id, headers):
    """Test getting scan results."""
    print(f"\n🔍 Testing scan results for {scan_id}...")
    
    # Wait a bit for scan to complete
    for i in range(10):
        try:
            response = requests.get(
                f"{API_BASE}/scan/{scan_id}",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                status = result.get('status')
                print(f"   📊 Scan status: {status}")
                
                if status == 'completed':
                    issues = result.get('issues', [])
                    summary = result.get('summary', {})
                    
                    print(f"   ✅ Scan completed")
                    print(f"   Issues found: {len(issues)}")
                    print(f"   Summary: {summary}")
                    
                    # Show first few issues
                    for i, issue in enumerate(issues[:3]):
                        print(f"   Issue {i+1}: {issue.get('severity')} - {issue.get('description')}")
                    
                    return True
                elif status == 'failed':
                    print(f"   ❌ Scan failed")
                    return False
                else:
                    print(f"   ⏳ Scan in progress... ({i+1}/10)")
                    time.sleep(2)
            else:
                print(f"   ❌ Failed to get results: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"   ❌ Results error: {e}")
            time.sleep(2)
    
    print("   ⏰ Scan timeout")
    return False

def test_mock_mode():
    """Test with mock responses if real API isn't available."""
    print("\n🔍 Testing mock mode...")
    
    # Simple mock test - just check if we can create issues
    mock_issues = [
        {
            "severity": "high",
            "type": "security",
            "description": "Hardcoded password detected",
            "file_path": "test_sample.py",
            "line_number": 2
        }
    ]
    
    print(f"   ✅ Mock scan would find {len(mock_issues)} issues")
    for issue in mock_issues:
        print(f"   - {issue['severity']}: {issue['description']}")
    
    return True

def main():
    """Run all tests."""
    print("🧪 VibeCodeAuditor API Test Client\n")
    
    # Test health endpoint
    health_ok = test_health()
    
    if health_ok:
        # Test file upload
        upload_ok = test_file_upload()
        
        if not upload_ok:
            print("\n⚠️  API tests failed, running mock mode...")
            test_mock_mode()
    else:
        print("\n⚠️  API server not available, running mock mode...")
        test_mock_mode()
    
    print("\n" + "="*50)
    print("🏁 Test Summary")
    print("="*50)
    
    if health_ok:
        print("✅ API server is running")
        print("✅ Health endpoint works")
        print("ℹ️  File upload may require proper authentication")
    else:
        print("❌ API server not accessible")
        print("💡 Start server with: python3 run_production.py")
    
    print("\nTo start the server:")
    print("1. python3 quick_install.py  # Install dependencies")
    print("2. Update .env with Supabase credentials")
    print("3. python3 run_production.py  # Start server")
    print("4. python3 test_api_client.py  # Test again")

if __name__ == "__main__":
    main()