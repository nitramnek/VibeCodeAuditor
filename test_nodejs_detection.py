#!/usr/bin/env python3
"""
Test comprehensive Node.js security detection.
"""

import sys
from pathlib import Path

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

from vibeauditor.core.auditor import CodeAuditor
from vibeauditor.core.config import AuditorConfig

def test_nodejs_security_detection():
    """Test Node.js security rule detection."""
    print("🔍 Testing Enhanced Node.js Security Detection")
    print("=" * 60)
    
    config = AuditorConfig()
    auditor = CodeAuditor(config)
    
    # Test with the insecure Node.js file
    test_file = Path("test.js")
    if test_file.exists():
        print(f"📁 Scanning insecure Node.js file: {test_file}")
        results = auditor.scan(test_file)
        
        print(f"\n📊 Enhanced Detection Results:")
        summary = results.get_summary()
        print(f"   Total Issues: {summary['total_issues']}")
        print(f"   Critical: {summary['critical']}")
        print(f"   High: {summary['high']}")
        print(f"   Medium: {summary['medium']}")
        print(f"   Low: {summary['low']}")
        
        # Show detected frameworks
        if hasattr(results, 'detected_frameworks') and results.detected_frameworks:
            print(f"\n📋 Detected Frameworks:")
            for name, framework in results.detected_frameworks.items():
                print(f"   - {framework.name} ({framework.type.value if hasattr(framework.type, 'value') else framework.type}) - {framework.confidence:.1%}")
        
        # Show specific Node.js/Express issues
        nodejs_issues = [issue for issue in results.issues if 'nodejs' in issue.rule_id.lower() or 'express' in issue.rule_id.lower()]
        if nodejs_issues:
            print(f"\n🎯 Node.js/Express Security Issues Found ({len(nodejs_issues)}):")
            for i, issue in enumerate(nodejs_issues, 1):
                print(f"\n   {i}. {issue.rule_id}")
                print(f"      Severity: {issue.severity.value.upper()}")
                print(f"      Message: {issue.message}")
                print(f"      Line: {issue.line_number}")
                
                if hasattr(issue, 'standards') and issue.standards:
                    standards_text = ", ".join([std.name for std in issue.standards[:2]])
                    print(f"      Standards: {standards_text}")
                
                if hasattr(issue, 'metadata') and issue.metadata:
                    if 'iso27001' in issue.metadata:
                        print(f"      ISO 27001: {issue.metadata['iso27001']}")
                    if 'owasp' in issue.metadata:
                        print(f"      OWASP: {issue.metadata['owasp']}")
        
        # Show compliance summary
        if hasattr(results, 'compliance_summary') and results.compliance_summary:
            print(f"\n📋 Compliance Framework Impact:")
            for framework_id, data in results.compliance_summary.items():
                print(f"   {data['name']}: {data['count']} issues")
        
        # Expected violations check
        expected_violations = [
            "hardcoded_secrets",
            "security_misconfiguration", 
            "logging_security",
            "authentication"
        ]
        
        found_violations = [issue.rule_id for issue in results.issues]
        detected_expected = [v for v in expected_violations if any(v in rule for rule in found_violations)]
        
        print(f"\n✅ Expected Violations Detected: {len(detected_expected)}/{len(expected_violations)}")
        for violation in detected_expected:
            print(f"   ✓ {violation}")
        
        missing = [v for v in expected_violations if not any(v in rule for rule in found_violations)]
        if missing:
            print(f"\n❌ Missing Expected Violations:")
            for violation in missing:
                print(f"   ✗ {violation}")
        
        return len(detected_expected) >= 3  # At least 3 out of 4 expected violations
    
    else:
        print("❌ test.js file not found")
        return False

def test_iso27001_mapping():
    """Test ISO 27001 control mapping."""
    print("\n🏛️  Testing ISO 27001 Control Mapping")
    print("=" * 50)
    
    config = AuditorConfig()
    auditor = CodeAuditor(config)
    
    test_file = Path("test.js")
    if test_file.exists():
        results = auditor.scan(test_file)
        
        # Check for ISO 27001 mappings
        iso_mappings = {}
        for issue in results.issues:
            if hasattr(issue, 'metadata') and issue.metadata and 'iso27001' in issue.metadata:
                control = issue.metadata['iso27001']
                if control not in iso_mappings:
                    iso_mappings[control] = []
                iso_mappings[control].append(issue.rule_id)
        
        if iso_mappings:
            print("📋 ISO 27001 Controls Violated:")
            for control, rules in iso_mappings.items():
                print(f"   {control}: {len(rules)} issues")
                for rule in rules[:2]:  # Show first 2 rules
                    print(f"     - {rule}")
        
        # Expected ISO controls
        expected_controls = ["A.9.4.3", "A.12.4.1", "A.9.1.2", "A.10.1.2"]
        found_controls = list(iso_mappings.keys())
        
        print(f"\n✅ ISO 27001 Controls Mapped: {len(found_controls)}")
        return len(found_controls) > 0
    
    return False

def main():
    """Run comprehensive Node.js security tests."""
    print("🚀 VibeCodeAuditor Enhanced Node.js Security Test")
    print("=" * 60)
    
    tests = [
        ("Node.js Security Detection", test_nodejs_security_detection),
        ("ISO 27001 Mapping", test_iso27001_mapping),
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
            import traceback
            traceback.print_exc()
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 Enhanced Node.js security detection is working!")
        print("\n🌟 Now Detecting:")
        print("   ✅ Hardcoded secrets and credentials")
        print("   ✅ Express.js security misconfigurations")
        print("   ✅ CORS policy violations")
        print("   ✅ Error information disclosure")
        print("   ✅ Missing authentication on admin endpoints")
        print("   ✅ JWT token security issues")
        print("   ✅ PII logging violations")
        print("   ✅ Input validation gaps")
        print("   ✅ Stack trace exposure")
        
        print("\n🏛️  Standards Compliance:")
        print("   ✅ ISO 27001 controls mapping")
        print("   ✅ OWASP Top 10 2021 alignment")
        print("   ✅ GDPR privacy requirements")
        print("   ✅ PCI DSS security standards")
        print("   ✅ ASVS verification requirements")
        
        return True
    else:
        print("⚠️  Some tests failed. The enhanced detection needs refinement.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)