#!/usr/bin/env python3
"""
Test the security scanner directly to see what it returns
"""
import sys
import asyncio
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

async def test_scanner():
    """Test the security scanner directly"""
    try:
        from vibeauditor.scanners.real_security_scanner import SecurityScanner
        
        print("🧪 Testing Security Scanner Directly")
        print("=" * 40)
        
        # Initialize scanner
        scanner = SecurityScanner()
        print("✅ Scanner initialized")
        
        # Test with the vulnerable JavaScript file
        test_file = Path("test_security_issues.js")
        if not test_file.exists():
            print("❌ Test file not found, creating it...")
            test_content = '''// Test JavaScript file with security vulnerabilities
const API_KEY = "sk-1234567890abcdef";
const PASSWORD = "admin123";

function updateContent(userInput) {
    document.getElementById('content').innerHTML = userInput; // XSS risk
}

function executeCode(code) {
    eval(code); // Very dangerous
}
'''
            test_file.write_text(test_content)
            print("✅ Created test file")
        
        print(f"🔍 Scanning file: {test_file}")
        
        # Run the scan
        results = await scanner.scan_file(str(test_file))
        
        print("📊 Scan Results:")
        print(f"   Type: {type(results)}")
        print(f"   Keys: {list(results.keys()) if isinstance(results, dict) else 'Not a dict'}")
        
        if isinstance(results, dict):
            issues = results.get("issues", [])
            print(f"   Issues found: {len(issues)}")
            
            if issues:
                print("\\n🔍 Issues Details:")
                for i, issue in enumerate(issues, 1):
                    print(f"   {i}. {issue}")
            else:
                print("   ⚠️ No issues found")
                
                # Let's check what each scanner returned
                print("\\n🔧 Debugging scanner results...")
                
                # Test custom rules scanner directly
                from vibeauditor.scanners.real_security_scanner import CustomRulesScanner
                custom_scanner = CustomRulesScanner()
                
                if custom_scanner.supports_files([test_file]):
                    print("✅ Custom scanner supports this file")
                    custom_result = await custom_scanner.scan([test_file])
                    print(f"   Custom scanner found: {len(custom_result.issues)} issues")
                    for issue in custom_result.issues:
                        print(f"     - {issue}")
                else:
                    print("❌ Custom scanner doesn't support this file")
        else:
            print(f"   Unexpected result type: {results}")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_scanner())