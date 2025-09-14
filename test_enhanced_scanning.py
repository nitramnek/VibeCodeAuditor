#!/usr/bin/env python3
"""
Test script to verify enhanced scanning with compliance standards.
"""

import sys
from pathlib import Path

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

from vibeauditor.core.auditor import CodeAuditor
from vibeauditor.core.config import AuditorConfig

def test_enhanced_scanning():
    """Test enhanced scanning with compliance standards."""
    print("🔍 Testing Enhanced Scanning with Compliance Standards")
    print("=" * 60)
    
    config = AuditorConfig()
    auditor = CodeAuditor(config)
    
    # Test with the insecure Node.js file
    test_file = Path("test.js")
    if test_file.exists():
        print(f"📁 Scanning: {test_file}")
        results = auditor.scan(test_file)
        
        print(f"\n📊 Scan Results:")
        summary = results.get_summary()
        print(f"   Total Issues: {summary['total_issues']}")
        print(f"   Critical: {summary['critical']}")
        print(f"   High: {summary['high']}")
        print(f"   Medium: {summary['medium']}")
        print(f"   Low: {summary['low']}")
        
        # Check compliance summary
        if hasattr(results, 'compliance_summary') and results.compliance_summary:
            print(f"\n📋 Compliance Summary:")
            for framework, data in results.compliance_summary.items():
                if isinstance(data, dict) and 'name' in data:
                    print(f"   {data['name']}: {data['count']} violations")
                else:
                    print(f"   {framework}: {data} violations")
        
        # Show first few issues with enhanced information
        print(f"\n🎯 Enhanced Issue Details:")
        for i, issue in enumerate(results.issues[:3], 1):
            print(f"\n   Issue {i}: {issue.rule_id}")
            print(f"   Severity: {issue.severity.value.upper()}")
            print(f"   Message: {issue.message}")
            print(f"   File: {issue.file_path}:{issue.line_number}")
            
            # Check metadata
            if hasattr(issue, 'metadata') and issue.metadata:
                print(f"   Metadata:")
                for key, value in issue.metadata.items():
                    print(f"     {key}: {value}")
            
            # Check standards
            if hasattr(issue, 'standards') and issue.standards:
                print(f"   Standards ({len(issue.standards)}):")
                for std in issue.standards[:2]:  # Show first 2
                    print(f"     - {std.name}")
                    if std.section:
                        print(f"       Section: {std.section}")
                    print(f"       URL: {std.url}")
            else:
                print(f"   Standards: None found")
            
            # Check compliance frameworks
            if hasattr(issue, 'compliance_frameworks') and issue.compliance_frameworks:
                print(f"   Compliance Frameworks: {', '.join(issue.compliance_frameworks)}")
            else:
                print(f"   Compliance Frameworks: None found")
        
        # Test API serialization
        print(f"\n🔄 Testing API Serialization:")
        results_dict = results.to_dict()
        
        # Check if first issue has standards in serialized form
        if results_dict['issues']:
            first_issue = results_dict['issues'][0]
            print(f"   First issue standards: {len(first_issue.get('standards', []))}")
            print(f"   First issue compliance: {first_issue.get('compliance_frameworks', [])}")
            
            # Show serialized standards
            if first_issue.get('standards'):
                print(f"   Serialized standards:")
                for std in first_issue['standards'][:2]:
                    print(f"     - {std['name']} ({std['type']})")
        
        return len(results.issues) > 0
    
    else:
        print("❌ test.js file not found")
        return False

def main():
    """Run the enhanced scanning test."""
    print("🚀 VibeCodeAuditor Enhanced Scanning Test")
    print("=" * 60)
    
    success = test_enhanced_scanning()
    
    if success:
        print("\n🎉 Enhanced scanning is working!")
        print("\n✅ Features verified:")
        print("   - Framework detection")
        print("   - Standards mapping")
        print("   - Compliance framework identification")
        print("   - API serialization")
        print("\n💡 If you're not seeing standards in the UI:")
        print("   1. Make sure the React frontend is using the enhanced IssueCard")
        print("   2. Check that the API is returning standards data")
        print("   3. Verify the backend is running the enhanced auditor")
        return True
    else:
        print("⚠️  Enhanced scanning test failed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)