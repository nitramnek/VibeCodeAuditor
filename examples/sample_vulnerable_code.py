"""
Sample vulnerable code for testing VibeCodeAuditor.
This file contains intentional security vulnerabilities and code quality issues.
"""

import os
import pickle
import hashlib
import random

# Security Issues
API_KEY = "sk-1234567890abcdef1234567890abcdef"  # Hardcoded secret
DATABASE_PASSWORD = "admin123"  # Weak password

def unsafe_sql_query(user_input):
    # SQL Injection vulnerability
    query = "SELECT * FROM users WHERE name = '" + user_input + "'"
    return query

def unsafe_pickle_load(data):
    # Unsafe pickle loading
    return pickle.loads(data)

def weak_crypto():
    # Weak cryptographic practices
    password = "secret123"
    hash_value = hashlib.md5(password.encode()).hexdigest()
    return hash_value

def insecure_random():
    # Insecure random number generation
    return random.random()

# Code Quality Issues
def very_long_function_with_high_complexity(data, option1, option2, option3, option4):
    # This function is intentionally long and complex
    result = []
    
    if option1:
        if option2:
            if option3:
                if option4:
                    for item in data:
                        if item > 10:
                            if item < 100:
                                if item % 2 == 0:
                                    result.append(item * 2)
                                else:
                                    result.append(item * 3)
                            else:
                                if item % 3 == 0:
                                    result.append(item / 2)
                                else:
                                    result.append(item / 3)
                        else:
                            if item > 0:
                                result.append(item + 10)
                            else:
                                result.append(item - 10)
                else:
                    for item in data:
                        result.append(item)
            else:
                for item in data:
                    result.append(item * 2)
        else:
            for item in data:
                result.append(item + 1)
    else:
        for item in data:
            result.append(item)
    
    return result

# Missing docstring
def function_without_docstring(x, y):
    return x + y

# AI/ML Issues
def unsafe_model_loading():
    # Loading model from untrusted source
    model_url = "http://untrusted-site.com/model.pkl"
    # This would be unsafe in real code
    return f"Loading model from {model_url}"

def biased_decision_logic(person):
    # Biased decision making
    if person['gender'] == 'male':
        return "approved"
    else:
        return "needs_review"

def privacy_violation():
    # Direct collection of sensitive data
    email = input("Enter your email: ")
    phone = input("Enter your phone: ")
    ssn = input("Enter your SSN: ")
    return {"email": email, "phone": phone, "ssn": ssn}

# Duplicate code blocks
def process_data_type_a(data):
    cleaned_data = []
    for item in data:
        if item is not None:
            if isinstance(item, str):
                cleaned_data.append(item.strip().lower())
            else:
                cleaned_data.append(str(item).strip().lower())
    return cleaned_data

def process_data_type_b(data):
    cleaned_data = []
    for item in data:
        if item is not None:
            if isinstance(item, str):
                cleaned_data.append(item.strip().lower())
            else:
                cleaned_data.append(str(item).strip().lower())
    return cleaned_data

# Unused imports (os is imported but not used meaningfully)
print("Sample vulnerable code loaded")