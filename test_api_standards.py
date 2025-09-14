#!/usr/bin/env python3
"""
Test API standards output.
"""

import sys
import requests
import json
from pathlib import Path

def test_api_standards():
    """Test that the API returns standards information."""
    print("🧪 Testing API Standards Output")
    print("=" * 40)
    
    # Test health check first
    try:
        response = requests.get("http://localhost:8000/api/health", timeout=5)
        if response.status_code != 200:
            print("❌ API server not running on localhost:8000")
            print("💡 Start the server with: python start_server.py")
            return False
        print("✅ API server is running")
    except Exception as e:
        print(f"❌ Cannot connect to API server: {e}")
        return False
    
    # Test file upload
    test_file = Path("test.js")
    if not test_file.exists():
        print("❌ test.js file not found")
        return False
    
    try:
        with open(test_file, 'rb') as f:
            files = {'files': f}
            response = requests.post("http://localhost:8000/api/scan/upload", files=files, timeout=30)
        
        if response.status_code != 200:
            print(f"❌ Upload failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
        
        scan_data = response.json()
        scan_id = scan_data.get('scan_id')
        print(f"✅ File uploaded, scan_id: {scan_id}")
        
        # Wait for scan to complete
        import time
        for i in range(10):  # Wait up to 10 seconds
            status_response = requests.get(f"http://localhost:8000/api/scan/{scan_id}/status", timeout=10)
            if status_response.status_code == 200:
                status_data = status_response.json()
                if status_data.get('status') == 'completed':
                    break
                print(f"⏳ Scan progress: {status_data.get('progress', 0)}%")
            time.sleep(1)
        
        # Get results
        results_response = requests.get(f"http://localhost:8000/api/scan/{scan_id}/results", timeout=10)
        if results_response.status_code != 200:
            print(f"❌ Results failed: {results_response.status_code}")
            return False
        
        results = results_response.json()
        print(f"✅ Results retrieved: {results['summary']['total_issues']} issues")
        
        # Check for standards information
        if results.get('issues'):
            first_issue = results['issues'][0]
            print(f"\n📋 First Issue: {first_issue.get('rule_id')}")
            print(f"   Message: {first_issue.get('message')}")
            
            # Check standards
            if first_issue.get('standards'):
                print(f"   Standards: {len(first_issue['standards'])} found")
                for std in first_issue['standards'][:2]:
                    print(f"     - {std.get('name')} ({std.get('type')})")
            else:
                print("   ❌ No standards information found")
            
            # Check metadata
            if first_issue.get('metadata'):
                metadata = first_issue['metadata']
                print(f"   Metadata:")
                for key, value in metadata.items():
                    print(f"     {key}: {value}")
            else:
                print("   ❌ No metadata found")
            
            # Check compliance frameworks
            if first_issue.get('compliance_frameworks'):
                print(f"   Compliance: {first_issue['compliance_frameworks']}")
            else:
                print("   ❌ No compliance frameworks found")
        
        # Check compliance summary
        if results.get('compliance_summary'):
            print(f"\n📊 Compliance Summary: {len(results['compliance_summary'])} frameworks affected")
            for framework_id, data in results['compliance_summary'].items():
                print(f"   {data.get('name', framework_id)}: {data.get('count', 0)} issues")
        else:
            print("\n❌ No compliance summary found")
        
        return True
        
    except Exception as e:
        print(f"❌ API test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_api_standards()
    print(f"\nResult: {'PASS' if success else 'FAIL'}")
    sys.exit(0 if success else 1)