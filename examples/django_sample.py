"""
Django sample with security vulnerabilities for testing framework-specific rules.
"""

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from django.db import connection
import os

# Configuration issues
DEBUG = True  # Should be False in production
SECRET_KEY = "weak123"  # Too short and weak
ALLOWED_HOSTS = []  # Should not be empty

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
        'PASSWORD': 'admin123',  # Hardcoded password
    }
}

def vulnerable_view(request):
    """View with multiple security issues."""
    
    # SQL Injection vulnerability
    user_id = request.GET.get('user_id')
    cursor = connection.cursor()
    query = f"SELECT * FROM users WHERE id = {user_id}"  # Vulnerable to SQL injection
    cursor.execute(query)
    
    # XSS vulnerability with mark_safe
    user_input = request.GET.get('message', '')
    safe_content = mark_safe(user_input)  # Dangerous without sanitization
    
    # Raw SQL usage
    raw_query = "SELECT * FROM sensitive_data WHERE user_id = %s" % user_id
    cursor.execute(raw_query)
    
    return HttpResponse(f"<h1>{safe_content}</h1>")

def admin_view(request):
    """Admin view without proper authentication."""
    # Missing @login_required decorator
    if request.user.is_staff:
        return render(request, 'admin.html')
    return HttpResponse("Access denied")

@login_required
def secure_view(request):
    """A more secure view example."""
    # Using parameterized query
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", [request.user.id])
    
    return render(request, 'secure.html', {
        'user': request.user
    })

# Settings that should be in environment variables
AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"  # Hardcoded AWS key
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

# Email configuration with hardcoded credentials
EMAIL_HOST_USER = 'admin@example.com'
EMAIL_HOST_PASSWORD = 'email_password_123'  # Should be in environment

# Session configuration issues
SESSION_COOKIE_SECURE = False  # Should be True for HTTPS
SESSION_COOKIE_HTTPONLY = False  # Should be True
CSRF_COOKIE_SECURE = False  # Should be True for HTTPS

# Logging configuration that might leak sensitive data
LOGGING = {
    'version': 1,
    'handlers': {
        'file': {
            'level': 'DEBUG',  # Too verbose for production
            'class': 'logging.FileHandler',
            'filename': 'django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',  # Will log sensitive information
        },
    },
}

if __name__ == "__main__":
    # Running with debug mode
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
    import django
    django.setup()
    
    # This would be vulnerable in production
    print(f"Secret key: {SECRET_KEY}")
    print(f"Debug mode: {DEBUG}")