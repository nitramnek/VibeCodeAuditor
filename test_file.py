#!/usr/bin/env python3
"""
Simple test file for upload testing
"""

# This is a test file with some potential security issues
API_KEY = "sk-1234567890abcdef"  # Hardcoded API key

def vulnerable_query(user_input):
    # SQL injection vulnerability
    query = "SELECT * FROM users WHERE id = " + user_input
    return query

def main():
    print("Hello, World!")
    unused_var = "This variable is not used"  # Unused variable
    
if __name__ == "__main__":
    main()