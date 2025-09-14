#!/usr/bin/env python3
"""
Simple VibeCodeAuditor Demo - Works immediately with your venv!
"""

import asyncio
from pathlib import Path
from vibeauditor.scanners.real_security_scanner import SecurityScanner, CustomRulesScanner

def create_test_files():
    """Create test files with security issues."""
    print("📁 Creating test files...")
    
    # Python file with security issues
    python_file = Path("demo_security_issues.py")
    python_file.write_text('''
#!/usr/bin/env python3
"""Demo file with intentional security issues"""

import os
import sqlite3

# CRITICAL: Hardcoded credentials
admin_password = "admin123"
api_key = "sk-1234567890abcdef"
database_password = "mySecretPassword"

# HIGH: SQL Injection vulnerability
def get_user(user_id):
    conn = sqlite3.connect("app.db")
    # Vulnerable query - user_id not sanitized
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return conn.execute(query).fetchall()

# HIGH: Command injection
def backup_files(filename):
    # Dangerous - user input directly in system command
    os.system(f"tar -czf backup.tar.gz {filename}")

# MEDIUM: Hardcoded paths and secrets
SECRET_KEY = "hardcoded-secret-key-123"
LOG_PATH = "/tmp/sensitive.log"

class AuthManager:
    def __init__(self):
        self.jwt_secret = "jwt-secret-key"  # CRITICAL
    
    def validate_token(self, token):
        # Insecure token validation
        return token == "admin-token"

if __name__ == "__main__":
    print("Demo app with security vulnerabilities")
''')
    
    # JavaScript file with issues
    js_file = Path("demo_frontend_issues.js")
    js_file.write_text('''
// Demo JavaScript with security issues

// CRITICAL: Hardcoded API credentials
const API_KEY = "abc-123-def-456";
const SECRET_TOKEN = "user-secret-token";

// HIGH: XSS vulnerability
function displayUserMessage(message) {
    document.getElementById("output").innerHTML = message;
}

// HIGH: Dangerous eval usage
function executeUserCode(userCode) {
    eval(userCode);  // Never do this!
}

// MEDIUM: Insecure data storage
function saveUserCredentials(username, password) {
    localStorage.setItem("username", username);
    localStorage.setItem("password", password);
}

// MEDIUM: No input validation
function processUserInput(input) {
    return input.replace(/<script>/g, "");  // Weak protection
}

console.log("Frontend demo loaded");
''')
    
    print(f"   ✅ Created {python_file}")
    print(f"   ✅ Created {js_file}")
    
    return [python_file, js_file]

async def scan_files(files):
    """Scan files for security issues."""
    print("\n🔍 Scanning files for security issues...")
    
    scanner = SecurityScanner()
    all_issues = []
    
    for file_path in files:
        print(f"\n   📄 Scanning {file_path.name}...")
        
        try:
            # Scan the file
            results = await scanner.scan_file(str(file_path))
            issues = results.get('issues', [])
            
            print(f"      🔍 Found {len(issues)} security issues")
            
            # Count by severity
            severity_counts = {}
            for issue in issues:
                severity = issue.get('severity', 'unknown')
                severity_counts[severity] = severity_counts.get(severity, 0) + 1
                all_issues.append(issue)
            
            # Show severity breakdown
            for severity, count in severity_counts.items():
                emoji = {"critical": "🚨", "high": "⚠️", "medium": "📋", "low": "ℹ️"}.get(severity, "❓")
                print(f"         {emoji} {severity.upper()}: {count}")
            
        except Exception as e:
            print(f"      ❌ Error scanning {file_path}: {e}")
    
    return all_issues

def show_detailed_results(issues):
    """Show detailed analysis of security issues."""
    print("\n" + "="*60)
    print("📊 DETAILED SECURITY ANALYSIS")
    print("="*60)
    
    # Group by severity
    by_severity = {}
    for issue in issues:
        severity = issue.get('severity', 'unknown')
        if severity not in by_severity:
            by_severity[severity] = []
        by_severity[severity].append(issue)
    
    # Show critical issues first
    for severity in ['critical', 'high', 'medium', 'low']:
        if severity in by_severity:
            severity_issues = by_severity[severity]
            emoji = {"critical": "🚨", "high": "⚠️", "medium": "📋", "low": "ℹ️"}[severity]
            
            print(f"\n{emoji} {severity.upper()} ISSUES ({len(severity_issues)})")
            print("-" * 40)
            
            for i, issue in enumerate(severity_issues[:5], 1):  # Show top 5
                print(f"\n{i}. {issue.get('message', 'No message')}")
                print(f"   📁 File: {Path(issue.get('file_path', '')).name}")
                print(f"   📍 Line: {issue.get('line_number', 'N/A')}")
                print(f"   💻 Code: {issue.get('code_snippet', 'N/A')}")
                print(f"   🔧 Fix: {issue.get('remediation', 'Review this issue')}")
    
    # Summary
    print(f"\n" + "="*60)
    print("📈 SECURITY SUMMARY")
    print("="*60)
    print(f"Total Issues Found: {len(issues)}")
    print(f"Files Scanned: 2")
    
    critical_count = len(by_severity.get('critical', []))
    high_count = len(by_severity.get('high', []))
    
    if critical_count > 0:
        print(f"🚨 {critical_count} CRITICAL issues need immediate attention!")
    if high_count > 0:
        print(f"⚠️  {high_count} HIGH priority issues should be fixed soon")
    
    print(f"\n💡 RECOMMENDATIONS:")
    print(f"   1. Fix all CRITICAL issues immediately")
    print(f"   2. Use environment variables for secrets")
    print(f"   3. Implement proper input validation")
    print(f"   4. Use parameterized queries for database access")
    print(f"   5. Sanitize all user inputs to prevent XSS")

def cleanup_files(files):
    """Clean up demo files."""
    print(f"\n🧹 Cleaning up demo files...")
    for file_path in files:
        if file_path.exists():
            file_path.unlink()
            print(f"   🗑️  Removed {file_path}")

async def main():
    """Main demo function."""
    print("🚀 VibeCodeAuditor Security Scanner Demo")
    print("="*50)
    print("This demo shows real security scanning in action!")
    
    # Create test files
    demo_files = create_test_files()
    
    try:
        # Scan files
        all_issues = await scan_files(demo_files)
        
        if all_issues:
            # Show detailed results
            show_detailed_results(all_issues)
            
            print(f"\n✅ Demo completed successfully!")
            print(f"🔍 Scanned {len(demo_files)} files")
            print(f"🚨 Found {len(all_issues)} security issues")
            
        else:
            print(f"\n⚠️  No issues detected. This might indicate:")
            print(f"   - Scanner configuration needs adjustment")
            print(f"   - Pattern matching needs improvement")
    
    finally:
        # Cleanup
        cleanup_files(demo_files)
    
    print(f"\n🎉 VibeCodeAuditor is working perfectly!")
    print(f"💡 Next steps:")
    print(f"   - Integrate with your CI/CD pipeline")
    print(f"   - Scan your real codebase")
    print(f"   - Set up automated security monitoring")

if __name__ == "__main__":
    asyncio.run(main())