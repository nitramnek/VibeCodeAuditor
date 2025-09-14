"""
Framework-specific audit rules with targeted guidance.
"""

import re
from pathlib import Path
from typing import List, Optional, Any, Dict

from .base_rule import BaseRule
from ..core.results import Issue, Severity
from ..core.framework_detector import Framework, FrameworkType
from .nodejs_security_rules import NodeJSRules

class DjangoSecurityRule(BaseRule):
    """Django-specific security checks."""
    
    def __init__(self):
        super().__init__(
            rule_id="django.security",
            description="Django framework security best practices",
            severity=Severity.HIGH,
            category="security"
        )
        self.languages = ['.py']
        self.framework = 'django'
    
    def check(self, file_path: Path, parsed_content: Optional[Any] = None) -> List[Issue]:
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.splitlines()
            
            # Check for Django-specific security issues
            django_checks = [
                (r'DEBUG\s*=\s*True', "Debug mode enabled in production", 
                 "Set DEBUG = False in production settings"),
                (r'SECRET_KEY\s*=\s*["\'][^"\']{1,20}["\']', "Weak or short SECRET_KEY", 
                 "Use a strong, randomly generated SECRET_KEY of at least 50 characters"),
                (r'ALLOWED_HOSTS\s*=\s*\[\s*\]', "Empty ALLOWED_HOSTS", 
                 "Configure ALLOWED_HOSTS with your domain names"),
                (r'django\.contrib\.admin.*without.*login_required', "Admin without authentication", 
                 "Ensure admin interface is properly protected"),
                (r'raw\s*\(.*\)', "Raw SQL query usage", 
                 "Use Django ORM instead of raw SQL to prevent injection attacks"),
                (r'mark_safe\s*\(', "Using mark_safe", 
                 "Be cautious with mark_safe() - ensure content is properly sanitized"),
            ]
            
            for line_num, line in enumerate(lines, 1):
                for pattern, message, remediation in django_checks:
                    if re.search(pattern, line, re.IGNORECASE):
                        issues.append(self.create_issue(
                            file_path=file_path,
                            message=f"Django Security: {message}",
                            line_number=line_num,
                            code_snippet=line.strip(),
                            remediation=f"{remediation}. See: https://docs.djangoproject.com/en/stable/topics/security/",
                            confidence=0.9,
                            metadata={
                                "framework": "django",
                                "security_category": "configuration",
                                "cwe": "CWE-16"  # Configuration
                            }
                        ))
        
        except Exception:
            pass
        
        return issues

class FlaskSecurityRule(BaseRule):
    """Flask-specific security checks."""
    
    def __init__(self):
        super().__init__(
            rule_id="flask.security",
            description="Flask framework security best practices",
            severity=Severity.HIGH,
            category="security"
        )
        self.languages = ['.py']
        self.framework = 'flask'
    
    def check(self, file_path: Path, parsed_content: Optional[Any] = None) -> List[Issue]:
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.splitlines()
            
            flask_checks = [
                (r'app\.debug\s*=\s*True', "Debug mode enabled", 
                 "Disable debug mode in production: app.debug = False"),
                (r'app\.run\(.*debug=True', "Debug mode in app.run()", 
                 "Remove debug=True from production code"),
                (r'SECRET_KEY\s*=\s*["\'][^"\']{1,20}["\']', "Weak SECRET_KEY", 
                 "Use a strong, randomly generated SECRET_KEY"),
                (r'render_template_string\s*\(.*request\.', "Template injection risk", 
                 "Avoid using user input directly in render_template_string()"),
                (r'@app\.route.*methods=.*GET.*POST', "Mixed HTTP methods", 
                 "Consider separating GET and POST handlers for better security"),
                (r'session\[.*\]\s*=.*request\.', "Unsafe session data", 
                 "Validate and sanitize data before storing in session"),
            ]
            
            for line_num, line in enumerate(lines, 1):
                for pattern, message, remediation in flask_checks:
                    if re.search(pattern, line, re.IGNORECASE):
                        issues.append(self.create_issue(
                            file_path=file_path,
                            message=f"Flask Security: {message}",
                            line_number=line_num,
                            code_snippet=line.strip(),
                            remediation=f"{remediation}. See: https://flask.palletsprojects.com/en/2.3.x/security/",
                            confidence=0.9,
                            metadata={
                                "framework": "flask",
                                "security_category": "configuration",
                                "cwe": "CWE-16"
                            }
                        ))
        
        except Exception:
            pass
        
        return issues

class TensorFlowSecurityRule(BaseRule):
    """TensorFlow-specific security and best practices."""
    
    def __init__(self):
        super().__init__(
            rule_id="tensorflow.security",
            description="TensorFlow ML security and best practices",
            severity=Severity.MEDIUM,
            category="ai_ml"
        )
        self.languages = ['.py']
        self.framework = 'tensorflow'
    
    def check(self, file_path: Path, parsed_content: Optional[Any] = None) -> List[Issue]:
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.splitlines()
            
            tf_checks = [
                (r'tf\.saved_model\.load\(.*http', "Loading model from HTTP", 
                 "Use HTTPS or local paths for model loading to prevent tampering"),
                (r'tf\.keras\.models\.load_model\(.*\.h5.*compile=False', "Loading model without compilation", 
                 "Consider security implications of loading uncompiled models"),
                (r'tf\.data\.Dataset\.from_generator.*without.*validation', "Unvalidated data pipeline", 
                 "Validate data inputs in your data pipeline"),
                (r'tf\.py_function\(.*func=.*lambda', "Unsafe py_function usage", 
                 "Be cautious with tf.py_function - ensure the function is safe"),
                (r'tf\.config\.experimental\.set_memory_growth\(.*False', "Memory growth disabled", 
                 "Consider enabling memory growth to prevent resource exhaustion"),
                (r'tf\.debugging\.set_log_device_placement\(True\)', "Device placement logging", 
                 "Disable device placement logging in production"),
            ]
            
            for line_num, line in enumerate(lines, 1):
                for pattern, message, remediation in tf_checks:
                    if re.search(pattern, line, re.IGNORECASE):
                        issues.append(self.create_issue(
                            file_path=file_path,
                            message=f"TensorFlow Security: {message}",
                            line_number=line_num,
                            code_snippet=line.strip(),
                            remediation=f"{remediation}. See: https://www.tensorflow.org/responsible_ai",
                            confidence=0.8,
                            metadata={
                                "framework": "tensorflow",
                                "security_category": "ml_security",
                                "cwe": "CWE-20"  # Improper Input Validation
                            }
                        ))
        
        except Exception:
            pass
        
        return issues

class PyTorchSecurityRule(BaseRule):
    """PyTorch-specific security checks."""
    
    def __init__(self):
        super().__init__(
            rule_id="pytorch.security",
            description="PyTorch ML security and best practices",
            severity=Severity.HIGH,
            category="ai_ml"
        )
        self.languages = ['.py']
        self.framework = 'pytorch'
    
    def check(self, file_path: Path, parsed_content: Optional[Any] = None) -> List[Issue]:
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.splitlines()
            
            pytorch_checks = [
                (r'torch\.load\([^)]*\)(?!.*map_location)', "Unsafe torch.load without map_location", 
                 "Always specify map_location in torch.load() to prevent arbitrary code execution"),
                (r'torch\.load\(.*http', "Loading model from HTTP", 
                 "Use HTTPS or local paths for model loading"),
                (r'pickle\.load.*\.pth', "Using pickle.load with .pth files", 
                 "Use torch.load() instead of pickle.load() for PyTorch models"),
                (r'torch\.jit\.load\(.*http', "Loading JIT model from HTTP", 
                 "Use secure sources for JIT model loading"),
                (r'torch\.hub\.load\(.*trust_repo=True', "Trusting repository without verification", 
                 "Verify repository authenticity before setting trust_repo=True"),
                (r'torch\.autograd\.set_grad_enabled\(False\).*eval\(\)', "Potential gradient leak", 
                 "Ensure proper context management for gradient computation"),
            ]
            
            for line_num, line in enumerate(lines, 1):
                for pattern, message, remediation in pytorch_checks:
                    if re.search(pattern, line, re.IGNORECASE):
                        issues.append(self.create_issue(
                            file_path=file_path,
                            message=f"PyTorch Security: {message}",
                            line_number=line_num,
                            code_snippet=line.strip(),
                            remediation=f"{remediation}. See: https://pytorch.org/docs/stable/notes/serialization.html",
                            confidence=0.9,
                            metadata={
                                "framework": "pytorch",
                                "security_category": "ml_security",
                                "cwe": "CWE-502"  # Deserialization of Untrusted Data
                            }
                        ))
        
        except Exception:
            pass
        
        return issues

class ReactSecurityRule(BaseRule):
    """React-specific security checks."""
    
    def __init__(self):
        super().__init__(
            rule_id="react.security",
            description="React framework security best practices",
            severity=Severity.MEDIUM,
            category="security"
        )
        self.languages = ['.js', '.jsx', '.ts', '.tsx']
        self.framework = 'react'
    
    def check(self, file_path: Path, parsed_content: Optional[Any] = None) -> List[Issue]:
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.splitlines()
            
            react_checks = [
                (r'dangerouslySetInnerHTML', "Using dangerouslySetInnerHTML", 
                 "Sanitize HTML content before using dangerouslySetInnerHTML"),
                (r'eval\s*\(', "Using eval()", 
                 "Avoid eval() - it can execute arbitrary code"),
                (r'innerHTML\s*=', "Direct innerHTML assignment", 
                 "Use React's JSX or textContent to prevent XSS"),
                (r'document\.write\s*\(', "Using document.write", 
                 "Avoid document.write - use React's rendering methods"),
                (r'window\.location\s*=.*user', "Unsafe redirect", 
                 "Validate URLs before redirecting to prevent open redirects"),
                (r'localStorage\.setItem\(.*password', "Storing sensitive data in localStorage", 
                 "Don't store sensitive data in localStorage - use secure storage"),
            ]
            
            for line_num, line in enumerate(lines, 1):
                for pattern, message, remediation in react_checks:
                    if re.search(pattern, line, re.IGNORECASE):
                        issues.append(self.create_issue(
                            file_path=file_path,
                            message=f"React Security: {message}",
                            line_number=line_num,
                            code_snippet=line.strip(),
                            remediation=f"{remediation}. See: https://reactjs.org/docs/dom-elements.html#dangerouslysetinnerhtml",
                            confidence=0.8,
                            metadata={
                                "framework": "react",
                                "security_category": "xss_prevention",
                                "cwe": "CWE-79"  # Cross-site Scripting
                            }
                        ))
        
        except Exception:
            pass
        
        return issues

class SQLAlchemySecurityRule(BaseRule):
    """SQLAlchemy-specific security checks."""
    
    def __init__(self):
        super().__init__(
            rule_id="sqlalchemy.security",
            description="SQLAlchemy ORM security best practices",
            severity=Severity.HIGH,
            category="security"
        )
        self.languages = ['.py']
        self.framework = 'sqlalchemy'
    
    def check(self, file_path: Path, parsed_content: Optional[Any] = None) -> List[Issue]:
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.splitlines()
            
            sqlalchemy_checks = [
                (r'session\.execute\(.*%.*\)', "String formatting in SQL", 
                 "Use parameterized queries instead of string formatting"),
                (r'session\.execute\(.*\.format\(', "String format in SQL", 
                 "Use parameterized queries with bound parameters"),
                (r'text\(.*%.*\)', "String formatting in text() SQL", 
                 "Use bound parameters with text() queries"),
                (r'engine\.execute\(.*\+.*\)', "String concatenation in SQL", 
                 "Use parameterized queries instead of string concatenation"),
                (r'create_engine\(.*echo=True', "SQL logging enabled", 
                 "Disable SQL logging in production (echo=False)"),
                (r'autocommit=True', "Autocommit enabled", 
                 "Be cautious with autocommit - prefer explicit transaction management"),
            ]
            
            for line_num, line in enumerate(lines, 1):
                for pattern, message, remediation in sqlalchemy_checks:
                    if re.search(pattern, line, re.IGNORECASE):
                        issues.append(self.create_issue(
                            file_path=file_path,
                            message=f"SQLAlchemy Security: {message}",
                            line_number=line_num,
                            code_snippet=line.strip(),
                            remediation=f"{remediation}. See: https://docs.sqlalchemy.org/en/14/core/tutorial.html#using-textual-sql",
                            confidence=0.9,
                            metadata={
                                "framework": "sqlalchemy",
                                "security_category": "sql_injection",
                                "cwe": "CWE-89"  # SQL Injection
                            }
                        ))
        
        except Exception:
            pass
        
        return issues

class FrameworkRules:
    """Collection of framework-specific rules."""
    
    @staticmethod
    def get_rules() -> List[BaseRule]:
        """Get all framework-specific rules."""
        rules = [
            DjangoSecurityRule(),
            FlaskSecurityRule(),
            TensorFlowSecurityRule(),
            PyTorchSecurityRule(),
            ReactSecurityRule(),
            SQLAlchemySecurityRule(),
        ]
        
        # Add comprehensive Node.js rules
        rules.extend(NodeJSRules.get_rules())
        
        return rules
    
    @staticmethod
    def get_rules_for_frameworks(frameworks: Dict[str, Framework]) -> List[BaseRule]:
        """Get rules specific to detected frameworks."""
        all_rules = FrameworkRules.get_rules()
        framework_names = set(frameworks.keys())
        
        # Return rules that match detected frameworks
        relevant_rules = []
        for rule in all_rules:
            if hasattr(rule, 'framework') and rule.framework in framework_names:
                relevant_rules.append(rule)
        
        return relevant_rules