#!/usr/bin/env python3
"""
Debug the scanner with actual uploaded content
"""
import sys
import re
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

def debug_scanner():
    """Debug scanner with actual content"""
    
    # Read the actual uploaded file
    file_path = "uploads/289c36cf-8779-4e49-bcfe-b829d0899472_test.js"
    
    if not Path(file_path).exists():
        print(f"❌ File not found: {file_path}")
        return
    
    content = Path(file_path).read_text()
    print("📁 File content (first 500 chars):")
    print(content[:500])
    print("\\n" + "="*50)
    
    # Test patterns
    patterns = [
        {
            'pattern': r'(password|PASSWORD|PASS)\s*[=:]\s*["\'][^"\']+["\']',
            'rule_id': 'hardcoded_password',
            'message': 'Hardcoded password detected'
        },
        {
            'pattern': r'(api[_-]?key|API[_-]?KEY|apiKey)\s*[=:]\s*["\'][^"\']+["\']',
            'rule_id': 'hardcoded_api_key',
            'message': 'Hardcoded API key detected'
        },
        {
            'pattern': r'(secret|SECRET|Secret)\s*[=:]\s*["\'][^"\']+["\']',
            'rule_id': 'hardcoded_secret',
            'message': 'Hardcoded secret detected'
        },
        {
            'pattern': r'eval\s*\(',
            'rule_id': 'dangerous_eval',
            'message': 'Use of eval() is dangerous'
        }
    ]
    
    print("🔍 Testing patterns against actual content:")
    print()
    
    lines = content.split('\\n')
    total_matches = 0
    
    for i, line in enumerate(lines, 1):
        line_matches = []
        
        for pattern_info in patterns:
            if re.search(pattern_info['pattern'], line, re.IGNORECASE):
                line_matches.append(pattern_info)
                total_matches += 1
        
        if line_matches:
            print(f"Line {i}: {line.strip()}")
            for match in line_matches:
                print(f"  ✅ {match['rule_id']}: {match['message']}")
            print()
    
    print(f"📊 Total matches found: {total_matches}")
    
    if total_matches == 0:
        print("\\n❌ No matches found. Let's check specific lines:")
        
        # Check specific lines that should match
        test_lines = [
            "const DB_PASS = 'changeme123';",
            "const JWT_SECRET = 'supersecretjwtkey';"
        ]
        
        for test_line in test_lines:
            print(f"\\nTesting: {test_line}")
            for pattern_info in patterns:
                match = re.search(pattern_info['pattern'], test_line, re.IGNORECASE)
                if match:
                    print(f"  ✅ Matches {pattern_info['rule_id']}: {match.group()}")
                else:
                    print(f"  ❌ No match for {pattern_info['rule_id']}")

if __name__ == "__main__":
    debug_scanner()