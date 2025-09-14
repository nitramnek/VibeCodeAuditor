#!/usr/bin/env python3
"""
Quick test of Node.js security detection.
"""

import sys
from pathlib import Path

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

def main():
    try:
        # Import after adding to path
        from vibeauditor.core.auditor import CodeAuditor
        from vibeauditor.core.config import AuditorConfig
        
        print("🔍 Quick Node.js Security Test")
        print("=" * 40)
        
        config = AuditorConfig()
        auditor = CodeAuditor(config)
        
        # Test with the insecure Node.js file
        test_file = Path("test.js")
        if not test_file.exists():
            print("❌ test.js file not found")
            return False
        
        print(f"📁 Scanning: {test_file}")
        results = auditor.scan(test_file)
        
        print(f"\n📊 Results:")
        summary = results.get_summary()
        print(f"   Total Issues: {summary['total_issues']}")
        print(f"   Critical: {summary['critical']}")
        print(f"   High: {summary['high']}")
        print(f"   Medium: {summary['medium']}")
        
        if results.issues:
            print(f"\n🎯 Issues Found:")
            for i, issue in enumerate(results.issues[:5], 1):  # Show first 5
                print(f"   {i}. {issue.rule_id}")
                print(f"      {issue.message}")
                print(f"      Line {issue.line_number}: {issue.code_snippet[:50]}...")
                
                # Show standards if available
                if hasattr(issue, 'metadata') and issue.metadata:
                    if 'iso27001' in issue.metadata:
                        print(f"      ISO 27001: {issue.metadata['iso27001']}")
                print()
        
        # Check if we found the expected issues
        rule_ids = [issue.rule_id for issue in results.issues]
        nodejs_rules = [r for r in rule_ids if 'nodejs' in r or 'express' in r]
        
        print(f"✅ Node.js/Express rules triggered: {len(nodejs_rules)}")
        
        if len(nodejs_rules) >= 3:
            print("🎉 Enhanced Node.js detection is working!")
            return True
        else:
            print("⚠️  Expected more Node.js security issues to be detected")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    print(f"\nResult: {'PASS' if success else 'FAIL'}")
    sys.exit(0 if success else 1)