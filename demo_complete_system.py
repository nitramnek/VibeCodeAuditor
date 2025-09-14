#!/usr/bin/env python3
"""
Complete system demonstration for VibeCodeAuditor.
Shows end-to-end functionality without external dependencies.
"""

import asyncio
import json
from pathlib import Path
from vibeauditor.core.results import Issue, Severity, AuditResults
from vibeauditor.scanners.real_security_scanner import SecurityScanner, CustomRulesScanner

def create_demo_files():
    """Create demonstration files with various security issues."""
    print("📁 Creating demo files with security issues...")
    
    # Python file with multiple security issues
    python_demo = Path("demo_python_issues.py")
    python_demo.write_text('''
#!/usr/bin/env python3
"""
Demo Python file with intentional security issues for testing.
"""

import os
import subprocess
import sqlite3

# SECURITY ISSUE: Hardcoded credentials
DATABASE_PASSWORD = "admin123"
API_KEY = "sk-1234567890abcdef"
SECRET_KEY = "my-super-secret-key"

# SECURITY ISSUE: SQL Injection vulnerability
def get_user_by_id(user_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    # Vulnerable to SQL injection
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)
    return cursor.fetchall()

# SECURITY ISSUE: Command injection
def backup_database(filename):
    # Dangerous use of os.system with user input
    os.system(f"mysqldump database > {filename}")

# SECURITY ISSUE: Insecure random number generation
import random
def generate_session_token():
    return random.randint(100000, 999999)

# SECURITY ISSUE: Hardcoded file paths
LOG_FILE = "/tmp/app.log"
CONFIG_FILE = "/etc/myapp/config.ini"

class UserManager:
    def __init__(self):
        self.admin_password = "password123"  # SECURITY ISSUE
    
    def authenticate(self, username, password):
        # SECURITY ISSUE: Timing attack vulnerability
        if username == "admin" and password == self.admin_password:
            return True
        return False

if __name__ == "__main__":
    print("Demo application with security issues")
''')
    
    # JavaScript file with security issues
    js_demo = Path("demo_javascript_issues.js")
    js_demo.write_text('''
// Demo JavaScript file with security issues

// SECURITY ISSUE: Hardcoded credentials
const API_KEY = "abc-123-def-456";
const PASSWORD = "secret123";

// SECURITY ISSUE: XSS vulnerability
function displayUserContent(userInput) {
    document.getElementById("content").innerHTML = userInput;
}

// SECURITY ISSUE: Dangerous eval usage
function executeUserCode(code) {
    eval(code);
}

// SECURITY ISSUE: Insecure localStorage usage
function storeCredentials(username, password) {
    localStorage.setItem("username", username);
    localStorage.setItem("password", password);
}

// SECURITY ISSUE: No input validation
function processUserData(data) {
    return data.replace(/script/g, "");  // Weak XSS protection
}

// SECURITY ISSUE: Hardcoded URLs
const API_ENDPOINT = "http://api.example.com/secret";
const ADMIN_URL = "https://admin.internal.com";

console.log("Demo JavaScript with security issues");
''')
    
    # Configuration file with secrets
    config_demo = Path("demo_config.yaml")
    config_demo.write_text('''
# Demo configuration with security issues

database:
  host: localhost
  username: admin
  password: "admin123"  # SECURITY ISSUE: Hardcoded password
  
api:
  key: "sk-1234567890abcdef"  # SECURITY ISSUE: Hardcoded API key
  secret: "my-secret-key"     # SECURITY ISSUE: Hardcoded secret
  
security:
  jwt_secret: "hardcoded-jwt-secret"  # SECURITY ISSUE
  encryption_key: "12345678901234567890123456789012"  # SECURITY ISSUE
  
external_services:
  aws_access_key: "AKIAIOSFODNN7EXAMPLE"  # SECURITY ISSUE
  aws_secret_key: "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"  # SECURITY ISSUE
''')
    
    print(f"   ✅ Created {python_demo}")
    print(f"   ✅ Created {js_demo}")
    print(f"   ✅ Created {config_demo}")
    
    return [python_demo, js_demo, config_demo]

async def demonstrate_scanning(files):
    """Demonstrate the security scanning functionality."""
    print("\n🔍 Demonstrating Security Scanning...")
    
    # Initialize scanner
    scanner = SecurityScanner()
    print("   ✅ Security scanner initialized")
    
    all_issues = []
    
    for file_path in files:
        print(f"\n   📄 Scanning {file_path}...")
        
        try:
            # Scan individual file
            results = await scanner.scan_file(str(file_path))
            issues = results.get('issues', [])
            
            print(f"      🔍 Found {len(issues)} security issues")
            
            # Display issues by severity
            severity_counts = {}
            for issue in issues:
                severity = issue.get('severity', 'unknown')
                severity_counts[severity] = severity_counts.get(severity, 0) + 1
                all_issues.append(issue)
            
            for severity, count in severity_counts.items():
                print(f"         {severity.upper()}: {count} issues")
            
            # Show top 3 issues for this file
            for i, issue in enumerate(issues[:3]):
                rule_id = issue.get('rule_id', 'unknown')
                message = issue.get('message', 'No message')
                line = issue.get('line_number', 0)
                print(f"         {i+1}. [{rule_id}] Line {line}: {message}")
        
        except Exception as e:
            print(f"      ❌ Scan failed: {e}")
    
    return all_issues

def generate_security_report(issues):
    """Generate a comprehensive security report."""
    print("\n📊 Generating Security Report...")
    
    # Categorize issues
    by_severity = {}
    by_type = {}
    by_file = {}
    
    for issue in issues:
        severity = issue.get('severity', 'unknown')
        rule_id = issue.get('rule_id', 'unknown')
        file_path = issue.get('file_path', 'unknown')
        
        by_severity[severity] = by_severity.get(severity, 0) + 1
        by_type[rule_id] = by_type.get(rule_id, 0) + 1
        by_file[file_path] = by_file.get(file_path, 0) + 1
    
    print(f"\n   📈 SECURITY SUMMARY")
    print(f"   {'='*40}")
    print(f"   Total Issues Found: {len(issues)}")
    print(f"   Files Scanned: {len(by_file)}")
    
    print(f"\n   🚨 ISSUES BY SEVERITY")
    print(f"   {'-'*25}")
    for severity in ['critical', 'high', 'medium', 'low']:
        count = by_severity.get(severity, 0)
        if count > 0:
            print(f"   {severity.upper():>8}: {count}")
    
    print(f"\n   🔍 TOP ISSUE TYPES")
    print(f"   {'-'*25}")
    sorted_types = sorted(by_type.items(), key=lambda x: x[1], reverse=True)
    for rule_id, count in sorted_types[:5]:
        clean_rule = rule_id.replace('custom_rules_', '').replace('_', ' ').title()
        print(f"   {clean_rule}: {count}")
    
    print(f"\n   📁 ISSUES BY FILE")
    print(f"   {'-'*25}")
    for file_path, count in by_file.items():
        filename = Path(file_path).name
        print(f"   {filename}: {count} issues")
    
    # Generate detailed report
    report = {
        "summary": {
            "total_issues": len(issues),
            "files_scanned": len(by_file),
            "severity_breakdown": by_severity,
            "top_issue_types": dict(sorted_types[:10])
        },
        "issues": issues
    }
    
    # Save report
    report_file = Path("security_report.json")
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n   💾 Detailed report saved to: {report_file}")
    
    return report

def demonstrate_issue_details(issues):
    """Show detailed information about specific issues."""
    print("\n🔍 DETAILED ISSUE ANALYSIS")
    print("="*50)
    
    # Group by severity for detailed display
    critical_issues = [i for i in issues if i.get('severity') == 'critical']
    high_issues = [i for i in issues if i.get('severity') == 'high']
    
    if critical_issues:
        print(f"\n🚨 CRITICAL ISSUES ({len(critical_issues)})")
        print("-" * 30)
        for i, issue in enumerate(critical_issues[:3], 1):
            print(f"\n{i}. {issue.get('message', 'No message')}")
            print(f"   File: {Path(issue.get('file_path', '')).name}")
            print(f"   Line: {issue.get('line_number', 'N/A')}")
            print(f"   Code: {issue.get('code_snippet', 'N/A')}")
            print(f"   Fix: {issue.get('remediation', 'Review and fix this issue')}")
    
    if high_issues:
        print(f"\n⚠️  HIGH PRIORITY ISSUES ({len(high_issues)})")
        print("-" * 30)
        for i, issue in enumerate(high_issues[:2], 1):
            print(f"\n{i}. {issue.get('message', 'No message')}")
            print(f"   File: {Path(issue.get('file_path', '')).name}")
            print(f"   Line: {issue.get('line_number', 'N/A')}")
            print(f"   Fix: {issue.get('remediation', 'Review and fix this issue')}")

async def main():
    """Main demonstration function."""
    print("🚀 VibeCodeAuditor Complete System Demonstration")
    print("="*60)
    
    # Create demo files
    demo_files = create_demo_files()
    
    # Demonstrate scanning
    all_issues = await demonstrate_scanning(demo_files)
    
    if all_issues:
        # Generate comprehensive report
        report = generate_security_report(all_issues)
        
        # Show detailed issue analysis
        demonstrate_issue_details(all_issues)
        
        print("\n" + "="*60)
        print("✅ DEMONSTRATION COMPLETE")
        print("="*60)
        print(f"📊 Scanned {len(demo_files)} files")
        print(f"🔍 Found {len(all_issues)} security issues")
        print(f"💾 Report saved to security_report.json")
        
        print("\n🎯 KEY FINDINGS:")
        critical_count = len([i for i in all_issues if i.get('severity') == 'critical'])
        high_count = len([i for i in all_issues if i.get('severity') == 'high'])
        
        if critical_count > 0:
            print(f"   🚨 {critical_count} CRITICAL issues require immediate attention")
        if high_count > 0:
            print(f"   ⚠️  {high_count} HIGH priority issues should be fixed soon")
        
        print("\n💡 NEXT STEPS:")
        print("   1. Review the detailed security_report.json")
        print("   2. Fix critical and high-priority issues first")
        print("   3. Implement secure coding practices")
        print("   4. Set up automated security scanning in CI/CD")
        
    else:
        print("\n⚠️  No issues found. This might indicate:")
        print("   - Scanner configuration issues")
        print("   - Missing security rules")
        print("   - Files don't contain detectable patterns")
    
    # Cleanup demo files
    print(f"\n🧹 Cleaning up demo files...")
    for file_path in demo_files:
        if file_path.exists():
            file_path.unlink()
            print(f"   🗑️  Removed {file_path}")

if __name__ == "__main__":
    asyncio.run(main())