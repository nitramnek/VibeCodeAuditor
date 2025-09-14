#!/usr/bin/env python3
"""
Test the enhanced standards display in the web interface.
"""

import sys
import requests
import json
import time
from pathlib import Path

def test_enhanced_display():
    """Test that the web interface shows enhanced standards information."""
    print("🌐 Testing Enhanced Web Interface Display")
    print("=" * 50)
    
    # Check if API server is running
    try:
        response = requests.get("http://localhost:8000/api/health", timeout=5)
        if response.status_code != 200:
            print("❌ API server not running. Start with: python start_server.py")
            return False
        print("✅ API server is running")
    except Exception as e:
        print(f"❌ Cannot connect to API: {e}")
        return False
    
    # Upload test file
    test_file = Path("test.js")
    if not test_file.exists():
        print("❌ test.js file not found")
        return False
    
    try:
        print("📤 Uploading test.js...")
        with open(test_file, 'rb') as f:
            files = {'files': f}
            response = requests.post("http://localhost:8000/api/scan/upload", files=files, timeout=30)
        
        if response.status_code != 200:
            print(f"❌ Upload failed: {response.status_code}")
            return False
        
        scan_data = response.json()
        scan_id = scan_data.get('scan_id')
        print(f"✅ Upload successful, scan_id: {scan_id}")
        
        # Wait for scan completion
        print("⏳ Waiting for scan to complete...")
        for i in range(15):  # Wait up to 15 seconds
            status_response = requests.get(f"http://localhost:8000/api/scan/{scan_id}/status", timeout=10)
            if status_response.status_code == 200:
                status_data = status_response.json()
                if status_data.get('status') == 'completed':
                    print("✅ Scan completed")
                    break
                print(f"   Progress: {status_data.get('progress', 0)}%")
            time.sleep(1)
        
        # Get results
        results_response = requests.get(f"http://localhost:8000/api/scan/{scan_id}/results", timeout=10)
        if results_response.status_code != 200:
            print(f"❌ Failed to get results: {results_response.status_code}")
            return False
        
        results = results_response.json()
        print(f"📊 Results: {results['summary']['total_issues']} issues found")
        
        # Analyze results for standards information
        standards_count = 0
        compliance_count = 0
        metadata_count = 0
        
        for issue in results.get('issues', []):
            if issue.get('standards'):
                standards_count += len(issue['standards'])
            if issue.get('compliance_frameworks'):
                compliance_count += len(issue['compliance_frameworks'])
            if issue.get('metadata'):
                metadata_count += 1
        
        print(f"\n📋 Standards Analysis:")
        print(f"   Issues with standards: {len([i for i in results.get('issues', []) if i.get('standards')])}")
        print(f"   Total standards references: {standards_count}")
        print(f"   Issues with compliance info: {len([i for i in results.get('issues', []) if i.get('compliance_frameworks')])}")
        print(f"   Issues with metadata: {metadata_count}")
        
        # Check for framework detection
        frameworks = results.get('detected_frameworks', {})
        print(f"   Detected frameworks: {len(frameworks)}")
        for name, framework in frameworks.items():
            print(f"     - {framework.get('name')} ({framework.get('confidence', 0):.1%})")
        
        # Check compliance summary
        compliance_summary = results.get('compliance_summary', {})
        print(f"   Compliance frameworks affected: {len(compliance_summary)}")
        for framework_id, data in compliance_summary.items():
            print(f"     - {data.get('name', framework_id)}: {data.get('count', 0)} issues")
        
        # Show sample issue with standards
        if results.get('issues'):
            first_issue = results['issues'][0]
            print(f"\n🔍 Sample Issue Analysis:")
            print(f"   Rule: {first_issue.get('rule_id')}")
            print(f"   Message: {first_issue.get('message')}")
            
            if first_issue.get('metadata'):
                metadata = first_issue['metadata']
                print(f"   Metadata keys: {list(metadata.keys())}")
                if 'iso27001' in metadata:
                    print(f"   ISO 27001: {metadata['iso27001']}")
                if 'owasp' in metadata:
                    print(f"   OWASP: {metadata['owasp']}")
                if 'cwe' in metadata:
                    print(f"   CWE: {metadata['cwe']}")
            
            if first_issue.get('standards'):
                print(f"   Standards: {len(first_issue['standards'])} found")
                for std in first_issue['standards'][:2]:
                    print(f"     - {std.get('name')} ({std.get('type')})")
        
        print(f"\n🌐 Web Interface URL:")
        print(f"   http://localhost:8000")
        print(f"   View results: http://localhost:8000/results/{scan_id}")
        
        # Success criteria
        success = (
            results['summary']['total_issues'] >= 10 and  # Should find many issues
            standards_count >= 20 and  # Should have many standards references
            len(frameworks) >= 2 and  # Should detect Node.js and Express
            len(compliance_summary) >= 2  # Should affect multiple compliance frameworks
        )
        
        if success:
            print("\n🎉 Enhanced display test PASSED!")
            print("   ✅ Multiple issues detected")
            print("   ✅ Standards information present")
            print("   ✅ Framework detection working")
            print("   ✅ Compliance summary generated")
        else:
            print("\n⚠️  Enhanced display test needs improvement")
            print(f"   Issues: {results['summary']['total_issues']} (need ≥10)")
            print(f"   Standards: {standards_count} (need ≥20)")
            print(f"   Frameworks: {len(frameworks)} (need ≥2)")
            print(f"   Compliance: {len(compliance_summary)} (need ≥2)")
        
        return success
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_enhanced_display()
    print(f"\nResult: {'PASS' if success else 'FAIL'}")
    sys.exit(0 if success else 1)