#!/usr/bin/env python3
"""
Test the security patterns directly
"""
import re

def test_patterns():
    """Test security patterns against our test content"""
    
    # Test content from our JavaScript file
    test_content = '''const API_KEY = "sk-1234567890abcdef";
const PASSWORD = "admin123";
const SECRET = "my-secret-key";
document.getElementById('content').innerHTML = userInput;
eval(code);
const DB_CONNECTION = "mongodb://admin:password123@localhost:27017/mydb";
apiKey: "AKIAIOSFODNN7EXAMPLE",
password: "supersecret123"'''
    
    # Updated patterns
    patterns = [
        {
            'pattern': r'(password|PASSWORD)\s*[=:]\s*["\'][^"\']+["\']',
            'rule_id': 'hardcoded_password',
            'message': 'Hardcoded password detected'
        },
        {
            'pattern': r'(api[_-]?key|API[_-]?KEY|apiKey)\s*[=:]\s*["\'][^"\']+["\']',
            'rule_id': 'hardcoded_api_key',
            'message': 'Hardcoded API key detected'
        },
        {
            'pattern': r'(secret[_-]?key|SECRET[_-]?KEY|secretKey|SECRET)\s*[=:]\s*["\'][^"\']+["\']',
            'rule_id': 'hardcoded_secret',
            'message': 'Hardcoded secret detected'
        },
        {
            'pattern': r'eval\s*\(',
            'rule_id': 'dangerous_eval',
            'message': 'Use of eval() is dangerous'
        },
        {
            'pattern': r'\.innerHTML\s*=',
            'rule_id': 'xss_innerHTML',
            'message': 'innerHTML assignment XSS risk'
        },
        {
            'pattern': r'(mongodb|postgresql|mysql)://[^"\'\\s]+:[^"\'\\s]+@',
            'rule_id': 'hardcoded_db_connection',
            'message': 'Hardcoded database connection'
        },
        {
            'pattern': r'AKIA[0-9A-Z]{16}',
            'rule_id': 'aws_access_key',
            'message': 'AWS Access Key detected'
        }
    ]
    
    print("🧪 Testing Security Patterns")
    print("=" * 30)
    
    lines = test_content.split('\\n')
    total_issues = 0
    
    for i, line in enumerate(lines, 1):
        print(f"Line {i}: {line}")
        line_issues = 0
        
        for pattern_info in patterns:
            if re.search(pattern_info['pattern'], line, re.IGNORECASE):
                print(f"  ✅ MATCH: {pattern_info['rule_id']} - {pattern_info['message']}")
                line_issues += 1
                total_issues += 1
        
        if line_issues == 0:
            print(f"  ❌ No matches")
        print()
    
    print(f"📊 Total issues found: {total_issues}")
    
    if total_issues > 0:
        print("🎉 Patterns are working!")
    else:
        print("❌ No patterns matched - need to debug")

if __name__ == "__main__":
    test_patterns()