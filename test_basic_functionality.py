#!/usr/bin/env python3
"""
Basic functionality test for VibeCodeAuditor.
"""

import sys
from pathlib import Path

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

from vibeauditor.core.auditor import CodeAuditor
from vibeauditor.core.config import AuditorConfig

def test_basic_scan():
    """Test basic scanning functionality."""
    print("🧪 Testing VibeCodeAuditor Basic Functionality")
    print("=" * 50)
    
    # Create default config
    config = AuditorConfig()
    print(f"✅ Created config with {len(config.include_patterns)} file patterns")
    
    # Initialize auditor
    auditor = CodeAuditor(config)
    print(f"✅ Initialized auditor with {len(auditor.rules)} rules")
    
    # Test with sample vulnerable code
    sample_file = Path("examples/sample_vulnerable_code.py")
    if not sample_file.exists():
        print("❌ Sample vulnerable code file not found")
        return False
    
    print(f"🔍 Scanning {sample_file}")
    results = auditor.scan(sample_file)
    
    # Print results
    summary = results.get_summary()
    print(f"\n📊 Scan Results:")
    print(f"   Total Issues: {summary['total_issues']}")
    print(f"   Critical: {summary['critical']}")
    print(f"   High: {summary['high']}")
    print(f"   Medium: {summary['medium']}")
    print(f"   Low: {summary['low']}")
    
    if summary['total_issues'] > 0:
        print(f"\n🔍 Sample Issues Found:")
        for i, issue in enumerate(results.issues[:3]):  # Show first 3 issues
            print(f"   {i+1}. {issue.rule_id}: {issue.message}")
            if issue.line_number:
                print(f"      Line {issue.line_number}")
    
    print(f"\n✅ Basic scan completed successfully!")
    return True

def test_cli_import():
    """Test CLI module import."""
    try:
        from vibeauditor.cli import main
        print("✅ CLI module imported successfully")
        return True
    except ImportError as e:
        print(f"❌ CLI import failed: {e}")
        return False

def test_api_import():
    """Test API module import."""
    try:
        from vibeauditor.api.main import app
        print("✅ API module imported successfully")
        return True
    except ImportError as e:
        print(f"❌ API import failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 VibeCodeAuditor Functionality Test")
    print("=" * 50)
    
    tests = [
        ("Basic Scan", test_basic_scan),
        ("CLI Import", test_cli_import),
        ("API Import", test_api_import),
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
        print("🎉 All tests passed! VibeCodeAuditor is ready to use.")
        print("\n🚀 Next steps:")
        print("   1. Run 'python run_server.py' to start the web interface")
        print("   2. Or use 'python -m vibeauditor scan <path>' for CLI")
        return True
    else:
        print("⚠️  Some tests failed. Check the error messages above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)