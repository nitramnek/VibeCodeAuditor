#!/usr/bin/env python3
"""
Fix the message field issue in main.py
"""

def fix_main_py():
    """Fix the message field in main.py"""
    
    # Read the current file
    with open("vibeauditor/main.py", "r") as f:
        content = f.read()
    
    # Replace the problematic line
    old_line = '"message": issue.get("description", issue.get("message", "")),'
    new_line = '"message": issue.get("description") or issue.get("message") or "Security issue detected",'
    
    # Replace all occurrences
    fixed_content = content.replace(old_line, new_line)
    
    # Write back the fixed content
    with open("vibeauditor/main.py", "w") as f:
        f.write(fixed_content)
    
    print("✅ Fixed message field in main.py")
    print("🔧 Changed:")
    print(f"   OLD: {old_line}")
    print(f"   NEW: {new_line}")
    print("\n🚀 Restart the server to apply the fix")

if __name__ == "__main__":
    fix_main_py()