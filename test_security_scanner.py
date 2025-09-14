#!/usr/bin/env python3
"""
Test the security scanner directly
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

async def test_scanner():
    """Test the security scanner with a sample file"""
    try:
        from vibeauditor.scanners.real_security_scanner import SecurityScanner
        
        print("🧪 Testing Security Scanner")
        print("=" * 40)
        
        # Initialize scanner
        scanner = SecurityScanner()
        print("✅ Scanner initialized")
        
        # Create a test file with security issues
        test_content = """
// Test JavaScript file with security issues
const express = require('express');
const app = express();

// Hardcoded secret (security issue)
const JWT_SECRET = 'supersecretkey123';

// SQL injection vulnerability
app.get('/user/:id', (req, res) => {
    const query = `SELECT * FROM users WHERE id = ${req.params.id}`;
    db.query(query, (err, results) => {
        if (err) {
            res.status(500).json({ error: err.message, stack: err.stack });
        } else {
            res.json(results);
        }
    });
});

app.listen(3000);
"""
        
        # Write test file
        test_file = Path("test_security_scan.js")
        test_file.write_text(test_content)
        print(f"✅ Created test file: {test_file}")
        
        # Run scan
        print("🔍 Running security scan...")
        results = await scanner.scan_file(str(test_file))
        
        print(f"✅ Scan completed!")
        print(f"📊 Results type: {type(results)}")
        print(f"📊 Results keys: {list(results.keys()) if isinstance(results, dict) else 'Not a dict'}")
        
        issues = results.get("issues", [])
        print(f"📊 Issues found: {len(issues)}")
        
        if issues:
            print("\n🔍 Issues details:")
            for i, issue in enumerate(issues, 1):
                print(f"  {i}. {issue.get('severity', 'unknown').upper()}: {issue.get('description', issue.get('message', 'No description'))}")
                if 'line_number' in issue:
                    print(f"     Line {issue['line_number']}: {issue.get('code_snippet', 'No snippet')}")
                if 'recommendation' in issue or 'remediation' in issue:
                    rec = issue.get('recommendation') or issue.get('remediation')
                    print(f"     Fix: {rec}")
                print()
        else:
            print("⚠️  No issues found - scanner might need configuration")
        
        # Cleanup
        test_file.unlink()
        print("🧹 Cleaned up test file")
        
        return len(issues) > 0
        
    except Exception as e:
        print(f"❌ Scanner test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Main test function"""
    success = await test_scanner()
    
    if success:
        print("\n✅ Security scanner is working!")
        print("🎯 The main server should now return issues")
    else:
        print("\n❌ Security scanner needs configuration")
        print("💡 The server will still work but may return empty issues")
    
    print("\n🚀 Restart the server with:")
    print("   source venv/bin/activate && python start_server.py")

if __name__ == "__main__":
    asyncio.run(main())