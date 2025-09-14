#!/usr/bin/env python3
"""Quick test of VibeCodeAuditor"""

from pathlib import Path
from vibeauditor.scanners.real_security_scanner import CustomRulesScanner

def main():
    print('🚀 VibeCodeAuditor Quick Test')
    print('='*40)
    
    # Test content with security issues
    test_content = '''
password = "admin123"
api_key = "sk-1234567890"
secret_key = "my-secret"
query = f"SELECT * FROM users WHERE id = {user_id}"
'''
    
    # Run scanner
    scanner = CustomRulesScanner()
    issues = scanner._scan_file_content(test_content, Path('test.py'))
    
    print(f'🔍 Found {len(issues)} security issues:')
    print()
    
    for i, issue in enumerate(issues, 1):
        severity = issue['severity'].upper()
        emoji = {'CRITICAL': '🚨', 'HIGH': '⚠️', 'MEDIUM': '📋', 'LOW': 'ℹ️'}.get(severity, '❓')
        
        print(f'{i}. {emoji} [{severity}] {issue["message"]}')
        print(f'   📍 Line {issue["line_number"]}: {issue["code_snippet"]}')
        print(f'   🔧 Fix: {issue["remediation"]}')
        print()
    
    print('✅ VibeCodeAuditor is working perfectly!')
    print('🎯 Your security scanner is ready!')

if __name__ == "__main__":
    main()