#!/usr/bin/env python3
"""
Test file with intentional security vulnerabilities for testing
"""
import os
import subprocess

# Hardcoded credentials (should trigger security alerts)
API_KEY = "sk-1234567890abcdef"
PASSWORD = "admin123"
SECRET_KEY = "my-secret-key-12345"

def vulnerable_function():
    """Function with security issues"""
    
    # SQL Injection vulnerability
    user_input = input("Enter user ID: ")
    query = f"SELECT * FROM users WHERE id = {user_input}"
    
    # Command injection vulnerability
    filename = input("Enter filename: ")
    os.system(f"cat {filename}")
    
    # Use of eval (dangerous)
    code = input("Enter Python code: ")
    eval(code)
    
    # Subprocess with shell=True
    subprocess.call(f"ls {filename}", shell=True)
    
    return query

def insecure_random():
    """Using weak random number generation"""
    import random
    return random.random()  # Should use secrets module instead

# Hardcoded database connection
DATABASE_URL = "postgresql://admin:password123@localhost/mydb"

if __name__ == "__main__":
    vulnerable_function()