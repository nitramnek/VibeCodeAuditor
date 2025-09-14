#!/usr/bin/env python3
"""
Standalone test for VibeCodeAuditor without external dependencies.
"""

import asyncio
import sys
from pathlib import Path

def test_security_scanner():
    """Test the security scanner directly."""
    print("🔍 Testing Security Scanner...")
    
    try:
        from vibeauditor.scanners.real_security_scanner import SecurityScanner
        from vibeauditor.core.results import Issue, Severity
        
        print("   ✅ Imports successful")
        
        # Create scanner instance
        scanner = SecurityScanner()
        print("   ✅ Scanner created")
        
        # Test with sample file
        test_file = Path("test_sample.py")
        if test_file.exists():
            print(f"   📁 Testing with {test_file}")
            
            # Run async scan
            async def run_scan():
                try:
                    results = await scanner.scan_file(str(test_file))
                    return results
                except Exception as e:
                    print(f"   ❌ Scan error: {e}")
                    return None
            
            # Run the scan
            results = asyncio.run(run_scan())
            
            if results:
                issues = results.get('issues', [])
                print(f"   ✅ Scan completed: {len(issues)} issues found")
                
                # Show first few issues
                for i, issue in enumerate(issues[:3]):
                    severity = issue.get('severity', 'unknown')
                    message = issue.get('message', 'No message')
                    print(f"   Issue {i+1}: [{severity}] {message}")
                
                return True
            else:
                print("   ❌ Scan failed")
                return False
        else:
            print("   ⚠️  No test file found")
            return False
            
    except Exception as e:
        print(f"   ❌ Scanner test failed: {e}")
        return False

def test_individual_scanners():
    """Test individual scanner components."""
    print("\n🔍 Testing Individual Scanners...")
    
    try:
        from vibeauditor.scanners.real_security_scanner import (
            BanditScanner, CustomRulesScanner
        )
        
        # Test Bandit scanner
        print("   Testing Bandit scanner...")
        bandit = BanditScanner()
        test_files = [Path("test_sample.py")]
        
        if bandit.supports_files(test_files):
            print("   ✅ Bandit supports Python files")
        
        # Test Custom Rules scanner
        print("   Testing Custom Rules scanner...")
        custom = CustomRulesScanner()
        
        if custom.supports_files(test_files):
            print("   ✅ Custom Rules supports all files")
        
        # Test custom rules directly
        async def test_custom():
            result = await custom.scan(test_files)
            return result
        
        custom_result = asyncio.run(test_custom())
        if custom_result and custom_result.issues:
            print(f"   ✅ Custom Rules found {len(custom_result.issues)} issues")
            for issue in custom_result.issues[:2]:
                print(f"      - {issue.get('rule_id')}: {issue.get('message')}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Individual scanner test failed: {e}")
        return False

def test_results_module():
    """Test the results data structures."""
    print("\n🔍 Testing Results Module...")
    
    try:
        from vibeauditor.core.results import Issue, Severity, AuditResults
        
        # Create test issue
        issue = Issue(
            rule_id="test_rule",
            severity=Severity.HIGH,
            category="security",
            message="Test security issue",
            file_path=Path("test.py"),
            line_number=10,
            code_snippet="password = 'secret'",
            remediation="Use environment variables"
        )
        
        print("   ✅ Issue created successfully")
        
        # Create results container
        results = AuditResults()
        results.add_issue(issue)
        
        print(f"   ✅ Results container: {len(results.issues)} issues")
        
        # Test serialization
        results_dict = results.to_dict()
        print(f"   ✅ Serialization: {len(results_dict['issues'])} issues in dict")
        
        # Test severity counts
        counts = results.get_severity_counts()
        print(f"   ✅ Severity counts: {counts}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Results module test failed: {e}")
        return False

def test_file_patterns():
    """Test security pattern detection."""
    print("\n🔍 Testing Security Pattern Detection...")
    
    test_content = '''
password = "admin123"
api_key = "sk-1234567890"
secret_key = "my-secret"
query = f"SELECT * FROM users WHERE id = {user_id}"
'''
    
    try:
        from vibeauditor.scanners.real_security_scanner import CustomRulesScanner
        
        scanner = CustomRulesScanner()
        
        # Test pattern detection
        issues = scanner._scan_file_content(test_content, Path("test.py"))
        
        print(f"   ✅ Pattern detection found {len(issues)} issues")
        
        expected_patterns = ["hardcoded_password", "hardcoded_api_key", "hardcoded_secret"]
        found_patterns = [issue['rule_id'] for issue in issues]
        
        for pattern in expected_patterns:
            if pattern in found_patterns:
                print(f"   ✅ Detected: {pattern}")
            else:
                print(f"   ⚠️  Missed: {pattern}")
        
        return len(issues) > 0
        
    except Exception as e:
        print(f"   ❌ Pattern detection test failed: {e}")
        return False

def main():
    """Run all standalone tests."""
    print("🧪 VibeCodeAuditor Standalone Tests\n")
    
    tests = [
        ("Results Module", test_results_module),
        ("Security Pattern Detection", test_file_patterns),
        ("Individual Scanners", test_individual_scanners),
        ("Full Security Scanner", test_security_scanner),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"   ❌ {name} crashed: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "="*50)
    print("📊 STANDALONE TEST SUMMARY")
    print("="*50)
    
    passed = 0
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {name}")
        if result:
            passed += 1
    
    print(f"\nPassed: {passed}/{len(results)} tests")
    
    if passed == len(results):
        print("\n🎉 All standalone tests passed!")
        print("The core security scanning functionality is working.")
        print("\nNext steps:")
        print("1. Set up Supabase credentials in .env")
        print("2. Test full API: python3 test_api_client.py")
        print("3. Start server: python3 run_production.py")
    else:
        print("\n⚠️  Some tests failed. Check the errors above.")
    
    return passed == len(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)