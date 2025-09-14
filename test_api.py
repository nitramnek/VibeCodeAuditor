#!/usr/bin/env python3
"""
Test script to verify VibeCodeAuditor API is working.
"""

import requests
import json
import time
from pathlib import Path

API_BASE = "http://localhost:8000"

def test_health_check():
    """Test API health check."""
    print("🏥 Testing health check...")
    try:
        response = requests.get(f"{API_BASE}/api/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_rules_endpoint():
    """Test rules endpoint."""
    print("📋 Testing rules endpoint...")
    try:
        response = requests.get(f"{API_BASE}/api/rules", timeout=10)
        if response.status_code == 200:
            rules = response.json()
            print(f"✅ Rules endpoint working: {len(rules)} rules found")
            for rule in rules[:3]:  # Show first 3 rules
                print(f"   - {rule['id']}: {rule['description'][:50]}...")
            return True
        else:
            print(f"❌ Rules endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Rules endpoint error: {e}")
        return False

def test_config_endpoint():
    """Test default config endpoint."""
    print("⚙️  Testing config endpoint...")
    try:
        response = requests.get(f"{API_BASE}/api/config/default", timeout=5)
        if response.status_code == 200:
            config = response.json()
            print(f"✅ Config endpoint working: min_severity={config.get('min_severity')}")
            return True
        else:
            print(f"❌ Config endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Config endpoint error: {e}")
        return False

def test_file_upload():
    """Test file upload and scanning."""
    print("📁 Testing file upload and scanning...")
    
    # Check if sample file exists
    sample_file = Path("examples/sample_vulnerable_code.py")
    if not sample_file.exists():
        print("❌ Sample file not found, skipping upload test")
        return False
    
    try:
        with open(sample_file, 'rb') as f:
            files = {'files': f}
            response = requests.post(f"{API_BASE}/api/scan/upload", files=files, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            scan_id = data.get('scan_id')
            print(f"✅ File upload successful: scan_id={scan_id}")
            
            # Wait a bit and check status
            time.sleep(2)
            status_response = requests.get(f"{API_BASE}/api/scan/{scan_id}/status", timeout=10)
            if status_response.status_code == 200:
                status_data = status_response.json()
                print(f"✅ Scan status: {status_data.get('status')} ({status_data.get('progress', 0)}%)")
                return True
            else:
                print(f"❌ Status check failed: {status_response.status_code}")
                return False
        else:
            print(f"❌ File upload failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ File upload error: {e}")
        return False

def main():
    """Run all API tests."""
    print("🧪 VibeCodeAuditor API Test Suite")
    print("=" * 40)
    
    tests = [
        ("Health Check", test_health_check),
        ("Rules Endpoint", test_rules_endpoint),
        ("Config Endpoint", test_config_endpoint),
        ("File Upload", test_file_upload),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running: {test_name}")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} ERROR: {e}")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All API tests passed! Your VibeCodeAuditor API is working correctly.")
        print("\n🌐 Next steps:")
        print("   1. Keep the API server running")
        print("   2. Run 'bash setup_webapp.sh' to setup the web interface")
        print("   3. Start the webapp with 'cd webapp && npm start'")
        return True
    else:
        print("⚠️  Some API tests failed. Check the error messages above.")
        print("💡 Make sure the API server is running: python start_server.py")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)