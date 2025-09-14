#!/usr/bin/env python3
"""
Test the scanner synchronously to debug issues
"""
import sys
import asyncio
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

async def test_sync_scanner():
    """Test scanner synchronously"""
    try:
        print("🧪 Testing Security Scanner Synchronously")
        print("=" * 50)
        
        # Import the scanner
        from vibeauditor.scanners.real_security_scanner import SecurityScanner, CustomRulesScanner
        
        # Test file path
        test_file = Path("uploads/289c36cf-8779-4e49-bcfe-b829d0899472_test.js")
        
        if not test_file.exists():
            print(f"❌ Test file not found: {test_file}")
            return
        
        print(f"📁 Testing file: {test_file}")
        print(f"📊 File size: {test_file.stat().st_size} bytes")
        
        # Read content
        content = test_file.read_text()
        print(f"📝 Content preview: {content[:200]}...")
        
        # Test custom rules scanner directly
        print("\\n🔧 Testing CustomRulesScanner directly...")
        custom_scanner = CustomRulesScanner()
        
        # Test if it supports the file
        supports = custom_scanner.supports_files([test_file])
        print(f"   Supports file: {supports}")
        
        if supports:
            # Run the scan
            result = await custom_scanner.scan([test_file])
            print(f"   Scanner result type: {type(result)}")
            print(f"   Issues found: {len(result.issues)}")
            print(f"   Errors: {result.errors}")
            
            if result.issues:
                print("\\n🚨 Issues found:")
                for i, issue in enumerate(result.issues, 1):
                    print(f"   {i}. {issue.get('rule_id', 'unknown')}: {issue.get('message', 'no message')}")
                    print(f"      Line {issue.get('line_number', '?')}: {issue.get('code_snippet', 'no snippet')}")
            else:
                print("   ❌ No issues found by custom scanner")
        
        # Test full security scanner
        print("\\n🔧 Testing full SecurityScanner...")
        scanner = SecurityScanner()
        
        # Run full scan
        full_results = await scanner.scan_file(str(test_file))
        print(f"   Full scan result type: {type(full_results)}")
        
        if isinstance(full_results, dict):
            issues = full_results.get("issues", [])
            print(f"   Total issues from full scan: {len(issues)}")
            
            if issues:
                print("\\n🎉 Full scan found issues:")
                for i, issue in enumerate(issues, 1):
                    print(f"   {i}. {issue}")
            else:
                print("   ❌ Full scan found no issues")
        else:
            print(f"   Unexpected result: {full_results}")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_sync_scanner())