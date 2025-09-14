#!/usr/bin/env python3
"""
Test script to verify API returns compliance standards data.
"""

import requests
import json
import time
from pathlib import Path

def test_api_compliance():
    """Test API compliance data."""
    print("🔍 Testing API Compliance Data")
    print("=" * 40)
    
    api_base = "http://localhost:8000"
    
    # Check if API is running
    try:
        response = requests.get(f"{api_base}/api/health")
        if response.status_code != 200:
            print("❌ API server not running. Start with: python start_server.py")
            return False
        print("✅ API server is running")
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API server. Start with: python start_server.py")
        return False
    
    # Upload test file
    test_file = Path("test.js")
    if not test_file.exists():
        print("❌ test.js file not found")
        return False
    
    print(f"📁 Uploading {test_file} for scanning...")
    
    with open(test_file, 'rb') as f:
        files = {'files': (test_file.name, f, 'application/javascript')}
        response = requests.post(f"{api_base}/api/scan/upload", files=files)
    
    if response.status_code != 200:
        print(f"❌ Upload failed: {response.text}")
        return False
    
    scan_data = response.json()
    scan_id = scan_data['scan_id']
    print(f"✅ Scan started: {scan_id}")
    
    # Wait for scan to complete
    print("⏳ Waiting for scan to complete...")
    max_wait = 30  # 30 seconds max
    wait_time = 0
    
    while wait_time < max_wait:
        response = requests.get(f"{api_base}/api/scan/{scan_id}/status")
        if response.status_code == 200:
            status_data = response.json()
            status = status_data['status']
            progress = status_data.get('progress', 0)
            
            print(f"   Status: {status} ({progress}%)")
            
            if status == 'completed':
                break
            elif status == 'failed':
                print(f"❌ Scan failed: {status_data.get('message', 'Unknown error')}")
                return False
        
        time.sleep(1)
        wait_time += 1
    
    if wait_time >= max_wait:
        print("❌ Scan timed out")
        return False
    
    # Get results
    print("📊 Fetching scan results...")
    response = requests.get(f"{api_base}/api/scan/{scan_id}/results")
    
    if response.status_code != 200:
        print(f"❌ Failed to get results: {response.text}")
        return False
    
    results = response.json()
    
    # Analyze results
    print(f"\n📈 Scan Summary:")
    summary = results['summary']
    print(f"   Total Issues: {summary['total_issues']}")
    print(f"   Critical: {summary['critical']}")
    print(f"   High: {summary['high']}")
    print(f"   Medium: {summary['medium']}")
    print(f"   Low: {summary['low']}")
    
    # Check compliance summary
    compliance_summary = results.get('compliance_summary', {})
    if compliance_summary:
        print(f"\n📋 Compliance Summary:")
        for framework, data in compliance_summary.items():
            if isinstance(data, dict):
                count = data.get('count', data.get('total_issues', 0))
                name = data.get('name', framework)
                print(f"   {name}: {count} violations")
            else:
                print(f"   {framework}: {data} violations")
    else:
        print(f"\n⚠️  No compliance summary found")
    
    # Check first few issues for standards data
    issues = results.get('issues', [])
    if issues:
        print(f"\n🎯 Issue Standards Analysis:")
        
        standards_found = 0
        compliance_found = 0
        
        for i, issue in enumerate(issues[:3], 1):
            print(f"\n   Issue {i}: {issue['rule_id']}")
            print(f"   Severity: {issue['severity'].upper()}")
            print(f"   Category: {issue['category']}")
            
            # Check metadata
            metadata = issue.get('metadata', {})
            if metadata:
                print(f"   Metadata: {list(metadata.keys())}")
                if 'iso27001' in metadata:
                    print(f"     ISO 27001: {metadata['iso27001']}")
                if 'owasp' in metadata:
                    print(f"     OWASP: {metadata['owasp']}")
                if 'cwe' in metadata:
                    print(f"     CWE: {metadata['cwe']}")
            
            # Check standards
            standards = issue.get('standards', [])
            if standards:
                standards_found += len(standards)
                print(f"   Standards ({len(standards)}):")
                for std in standards[:2]:  # Show first 2
                    print(f"     - {std['name']}")
                    if std.get('section'):
                        print(f"       Section: {std['section']}")
            else:
                print(f"   Standards: None")
            
            # Check compliance frameworks
            compliance_frameworks = issue.get('compliance_frameworks', [])
            if compliance_frameworks:
                compliance_found += len(compliance_frameworks)
                print(f"   Compliance: {', '.join(compliance_frameworks)}")
            else:
                print(f"   Compliance: None")
        
        print(f"\n📊 Standards Summary:")
        print(f"   Total standards found: {standards_found}")
        print(f"   Total compliance frameworks: {compliance_found}")
        
        if standards_found == 0 and compliance_found == 0:
            print(f"\n⚠️  No standards or compliance data found!")
            print(f"   This suggests the standards mapper is not working properly.")
            print(f"   Check the backend auditor implementation.")
            return False
        else:
            print(f"\n✅ Standards and compliance data found!")
            return True
    
    else:
        print(f"\n⚠️  No issues found in scan results")
        return False

def main():
    """Run the API compliance test."""
    print("🚀 VibeCodeAuditor API Compliance Test")
    print("=" * 50)
    
    success = test_api_compliance()
    
    if success:
        print("\n🎉 API compliance data is working!")
        print("\n💡 Next steps:")
        print("   1. Start the React frontend: cd webapp && npm start")
        print("   2. Upload a file and check if standards are visible in UI")
        print("   3. Look for compliance badges and expandable sections")
    else:
        print("\n❌ API compliance test failed")
        print("\n🔧 Troubleshooting:")
        print("   1. Make sure API server is running: python start_server.py")
        print("   2. Check that test.js file exists")
        print("   3. Verify backend standards mapper is working")
    
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)