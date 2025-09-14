"""
Enterprise-grade sample with multiple compliance and security issues.
This file demonstrates comprehensive standards mapping across various frameworks.
"""

import os
import hashlib
import pickle
import sqlite3
import logging
from datetime import datetime
from typing import Dict, Any, Optional

# GDPR/HIPAA Compliance Issues
class UserDataProcessor:
    """Processes user data with privacy compliance issues."""
    
    def __init__(self):
        # Hardcoded credentials - PCI DSS violation
        self.db_password = "admin123"
        self.api_key = "sk-1234567890abcdef1234567890abcdef"
        self.encryption_key = "weak_key_123"  # Weak encryption
        
        # Logging sensitive data - GDPR Article 32 violation
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)
    
    def process_personal_data(self, email: str, phone: str, ssn: str, 
                            medical_record: str) -> Dict[str, Any]:
        """Process personal data with multiple compliance violations."""
        
        # GDPR Article 25 violation - no data minimization
        user_data = {
            'email': email,
            'phone': phone,
            'ssn': ssn,  # PII without encryption
            'medical_record': medical_record,  # HIPAA violation
            'timestamp': datetime.now(),
            'ip_address': '192.168.1.1',  # Unnecessary data collection
            'browser_fingerprint': 'chrome_fingerprint_123'
        }
        
        # HIPAA 164.312 violation - unencrypted PHI storage
        with open('/tmp/medical_data.txt', 'w') as f:
            f.write(f"Medical record: {medical_record}")
        
        # GDPR logging violation - logging personal data
        self.logger.info(f"Processing data for user: {email}")
        self.logger.debug(f"Full user data: {user_data}")
        
        return user_data
    
    def weak_encryption(self, data: str) -> str:
        """Weak cryptographic implementation - NIST 800-53 SC violation."""
        # MD5 is cryptographically broken
        return hashlib.md5(data.encode()).hexdigest()
    
    def unsafe_data_storage(self, user_data: Dict) -> None:
        """Unsafe data storage - multiple compliance violations."""
        
        # Pickle serialization vulnerability - OWASP A08
        with open('/tmp/user_data.pkl', 'wb') as f:
            pickle.dump(user_data, f)
        
        # World-readable file permissions - ISO 27001 A.12 violation
        os.chmod('/tmp/user_data.pkl', 0o777)

class DatabaseManager:
    """Database operations with SQL injection vulnerabilities."""
    
    def __init__(self):
        # Hardcoded database credentials - PCI DSS Req 6 violation
        self.connection_string = "sqlite:///app.db?password=admin123"
        self.conn = sqlite3.connect('app.db')
    
    def get_user_data(self, user_id: str) -> Any:
        """SQL injection vulnerability - OWASP A03, SANS CWE-89."""
        cursor = self.conn.cursor()
        
        # Direct string concatenation - SQL injection
        query = f"SELECT * FROM users WHERE id = '{user_id}'"
        cursor.execute(query)
        
        return cursor.fetchall()
    
    def update_user_preferences(self, user_id: str, preferences: str) -> None:
        """Another SQL injection with string formatting."""
        cursor = self.conn.cursor()
        
        # String formatting in SQL - ASVS V5 violation
        query = "UPDATE users SET preferences = '%s' WHERE id = %s" % (preferences, user_id)
        cursor.execute(query)
        
        # No transaction management - ACID violation
        # Missing commit() - data integrity issue

class AuthenticationSystem:
    """Authentication with multiple security flaws."""
    
    def __init__(self):
        # Weak session configuration - OWASP A07
        self.session_timeout = 86400 * 7  # 7 days - too long
        self.failed_attempts = {}
        
    def authenticate_user(self, username: str, password: str) -> bool:
        """Weak authentication - NIST 800-53 AC violation."""
        
        # No rate limiting - brute force vulnerability
        # No account lockout mechanism
        
        # Weak password validation
        if len(password) < 6:  # Too short minimum
            return False
        
        # Hardcoded admin credentials - ASVS V2 violation
        if username == "admin" and password == "admin123":
            return True
        
        # Timing attack vulnerability - constant time comparison missing
        stored_password = self.get_stored_password(username)
        return password == stored_password
    
    def get_stored_password(self, username: str) -> Optional[str]:
        """Password storage with vulnerabilities."""
        
        # Passwords stored in plain text - OWASP A02
        passwords = {
            "user1": "password123",
            "user2": "qwerty",
            "admin": "admin123"
        }
        
        return passwords.get(username)
    
    def generate_session_token(self) -> str:
        """Weak session token generation."""
        import random
        
        # Using insecure random - not cryptographically secure
        return str(random.randint(100000, 999999))

class APIEndpoint:
    """API with multiple security vulnerabilities."""
    
    def __init__(self):
        self.db = DatabaseManager()
        self.auth = AuthenticationSystem()
        
    def process_user_input(self, user_input: str) -> str:
        """XSS vulnerability - OWASP A03, SANS CWE-79."""
        
        # No input validation - ASVS V5 violation
        # Direct output without encoding - XSS vulnerability
        return f"<div>User said: {user_input}</div>"
    
    def file_upload(self, filename: str, content: bytes) -> str:
        """Unsafe file upload - OWASP A01."""
        
        # No file type validation
        # No size limits
        # Directory traversal vulnerability
        file_path = f"/uploads/{filename}"
        
        with open(file_path, 'wb') as f:
            f.write(content)
        
        return file_path
    
    def proxy_request(self, url: str) -> str:
        """SSRF vulnerability - OWASP A10."""
        import requests
        
        # No URL validation - SSRF vulnerability
        # Could access internal services
        response = requests.get(url)
        return response.text

class LoggingSystem:
    """Logging with security and compliance issues."""
    
    def __init__(self):
        # Excessive logging level in production - OWASP A09
        logging.basicConfig(
            level=logging.DEBUG,  # Too verbose for production
            format='%(asctime)s - %(message)s',
            filename='/var/log/app.log'
        )
        self.logger = logging.getLogger(__name__)
    
    def log_user_activity(self, user_id: str, action: str, 
                         sensitive_data: Dict[str, Any]) -> None:
        """Logging sensitive information - multiple violations."""
        
        # GDPR violation - logging personal data
        # HIPAA violation - logging medical information
        # PCI DSS violation - logging payment data
        self.logger.info(f"User {user_id} performed {action}")
        self.logger.debug(f"Sensitive data: {sensitive_data}")
        
        # No log rotation - disk space issues
        # No log integrity protection - SOX 404 violation

class ConfigurationManager:
    """Configuration with security misconfigurations."""
    
    def __init__(self):
        # Debug mode in production - OWASP A05
        self.DEBUG = True
        
        # Insecure defaults - ISO 27001 A.14 violation
        self.ALLOWED_HOSTS = ['*']  # Too permissive
        self.CORS_ALLOW_ALL = True
        
        # Weak security headers
        self.SECURE_SSL_REDIRECT = False
        self.SESSION_COOKIE_SECURE = False
        self.CSRF_COOKIE_SECURE = False
        
        # Exposed sensitive information
        self.SECRET_KEY = "weak_secret_123"
        self.DATABASE_URL = "postgresql://admin:password@localhost/db"

def main():
    """Main function demonstrating multiple vulnerabilities."""
    
    # Initialize vulnerable components
    data_processor = UserDataProcessor()
    db_manager = DatabaseManager()
    auth_system = AuthenticationSystem()
    api = APIEndpoint()
    logger = LoggingSystem()
    config = ConfigurationManager()
    
    # Demonstrate vulnerabilities
    print("🚨 Running enterprise sample with multiple compliance violations...")
    
    # GDPR/HIPAA violations
    user_data = data_processor.process_personal_data(
        email="john.doe@example.com",
        phone="+1-555-0123",
        ssn="123-45-6789",
        medical_record="Patient has diabetes"
    )
    
    # Weak encryption
    encrypted = data_processor.weak_encryption("sensitive_data")
    print(f"Weakly encrypted data: {encrypted}")
    
    # SQL injection
    user_info = db_manager.get_user_data("1' OR '1'='1")
    
    # Authentication bypass
    is_authenticated = auth_system.authenticate_user("admin", "admin123")
    
    # XSS vulnerability
    html_output = api.process_user_input("<script>alert('XSS')</script>")
    
    # Logging violations
    logger.log_user_activity("user123", "login", user_data)
    
    print("✅ Sample execution completed - multiple violations detected!")

if __name__ == "__main__":
    main()