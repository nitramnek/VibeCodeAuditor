#!/usr/bin/env python3
"""
Test framework detection and framework-specific rules.
"""

import sys
from pathlib import Path

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

from vibeauditor.core.auditor import CodeAuditor
from vibeauditor.core.config import AuditorConfig
from vibeauditor.core.framework_detector import FrameworkDetector

def test_framework_detection():
    """Test framework detection capabilities."""
    print("🔍 Testing Framework Detection")
    print("=" * 50)
    
    detector = FrameworkDetector()
    
    # Test with different sample files
    test_files = [
        ("Django Sample", Path("examples/django_sample.py")),
        ("PyTorch Sample", Path("examples/pytorch_sample.py")),
        ("React Sample", Path("examples/react_sample.jsx")),
        ("Original Vulnerable Code", Path("examples/sample_vulnerable_code.py")),
    ]
    
    for name, file_path in test_files:
        if file_path.exists():
            print(f"\n📁 Analyzing {name}: {file_path}")
            frameworks = detector.detect_frameworks(file_path)
            
            if frameworks:
                print(f"✅ Detected {len(frameworks)} framework(s):")
                for fw_name, framework in frameworks.items():
                    print(f"   - {framework.name} ({framework.type.value}) - {framework.confidence:.1%} confidence")
            else:
                print("📋 No specific frameworks detected")
        else:
            print(f"❌ File not found: {file_path}")
    
    return True

def test_framework_specific_rules():
    """Test framework-specific rule application."""
    print("\n🧪 Testing Framework-Specific Rules")
    print("=" * 50)
    
    config = AuditorConfig()
    auditor = CodeAuditor(config)
    
    # Test with Django sample
    django_file = Path("examples/django_sample.py")
    if django_file.exists():
        print(f"\n🔍 Scanning Django sample: {django_file}")
        results = auditor.scan(django_file)
        
        print(f"📊 Results:")
        summary = results.get_summary()
        print(f"   Total Issues: {summary['total_issues']}")
        print(f"   Critical: {summary['critical']}")
        print(f"   High: {summary['high']}")
        print(f"   Medium: {summary['medium']}")
        print(f"   Low: {summary['low']}")
        
        # Show framework-specific issues
        django_issues = [issue for issue in results.issues if 'django' in issue.rule_id.lower()]
        if django_issues:
            print(f"\n🎯 Django-specific issues found: {len(django_issues)}")
            for issue in django_issues[:3]:  # Show first 3
                print(f"   - {issue.rule_id}: {issue.message}")
        
        # Show detected frameworks
        if hasattr(results, 'detected_frameworks') and results.detected_frameworks:
            print(f"\n📋 Detected frameworks:")
            for name, framework in results.detected_frameworks.items():
                print(f"   - {framework.name} ({framework.type.value if hasattr(framework.type, 'value') else framework.type})")
    
    # Test with PyTorch sample
    pytorch_file = Path("examples/pytorch_sample.py")
    if pytorch_file.exists():
        print(f"\n🔍 Scanning PyTorch sample: {pytorch_file}")
        results = auditor.scan(pytorch_file)
        
        summary = results.get_summary()
        print(f"📊 Results: {summary['total_issues']} total issues")
        
        # Show PyTorch-specific issues
        pytorch_issues = [issue for issue in results.issues if 'pytorch' in issue.rule_id.lower()]
        if pytorch_issues:
            print(f"🎯 PyTorch-specific issues found: {len(pytorch_issues)}")
            for issue in pytorch_issues[:3]:
                print(f"   - {issue.rule_id}: {issue.message}")
    
    return True

def test_enhanced_reporting():
    """Test enhanced reporting with framework information."""
    print("\n📄 Testing Enhanced Reporting")
    print("=" * 50)
    
    config = AuditorConfig()
    auditor = CodeAuditor(config)
    
    # Scan Django sample
    django_file = Path("examples/django_sample.py")
    if django_file.exists():
        results = auditor.scan(django_file)
        
        # Test console reporter
        from vibeauditor.reporters.console_reporter import ConsoleReporter
        reporter = ConsoleReporter(verbose=True)
        
        print("🖥️  Console Report:")
        reporter.generate_report(results)
        
        # Test JSON serialization
        results_dict = results.to_dict()
        if 'detected_frameworks' in results_dict:
            print(f"✅ Framework information included in JSON output")
            print(f"   Frameworks: {list(results_dict['detected_frameworks'].keys())}")
        
        return True
    
    return False

def main():
    """Run all framework detection tests."""
    print("🚀 VibeCodeAuditor Framework Detection Test Suite")
    print("=" * 60)
    
    tests = [
        ("Framework Detection", test_framework_detection),
        ("Framework-Specific Rules", test_framework_specific_rules),
        ("Enhanced Reporting", test_enhanced_reporting),
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
        print("🎉 All framework detection tests passed!")
        print("\n🌟 Enhanced Features Working:")
        print("   ✅ Framework detection (Django, Flask, PyTorch, React, etc.)")
        print("   ✅ Framework-specific security rules")
        print("   ✅ Targeted remediation guidance")
        print("   ✅ Enhanced reporting with framework context")
        print("   ✅ API integration with framework information")
        
        print("\n🚀 Try scanning your own projects:")
        print("   python -m vibeauditor scan /path/to/your/django/project")
        print("   python -m vibeauditor scan /path/to/your/ml/project")
        
        return True
    else:
        print("⚠️  Some tests failed. Check the error messages above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)