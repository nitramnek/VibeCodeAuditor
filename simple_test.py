#!/usr/bin/env python3
import re

# Test the pattern directly
content = "const DB_PASS = 'changeme123';"
pattern = r'(password|PASSWORD|PASS)\s*[=:]\s*["\'][^"\']+["\']'

match = re.search(pattern, content, re.IGNORECASE)
print(f"Content: {content}")
print(f"Pattern: {pattern}")
print(f"Match found: {bool(match)}")
if match:
    print(f"Matched text: {match.group()}")
else:
    print("No match - let's debug the pattern")
    
    # Test simpler patterns
    simple_patterns = [
        r'PASS',
        r'PASS\s*=',
        r'PASS\s*=\s*["\']',
        r'(PASS)\s*=\s*["\'][^"\']+["\']'
    ]
    
    for i, p in enumerate(simple_patterns):
        m = re.search(p, content, re.IGNORECASE)
        print(f"Pattern {i+1} ({p}): {'✅' if m else '❌'}")