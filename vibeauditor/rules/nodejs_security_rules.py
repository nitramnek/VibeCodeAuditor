"""
Comprehensive Node.js and Express.js security rules.
Maps to ISO 27001, OWASP, and other security standards.
"""

import re
from pathlib import Path
from typing import List, Optional, Any

from .base_rule import BaseRule
from ..core.results import Issue, Severity

class NodeJSHardcodedSecretsRule(BaseRule):
    """Detect hardcoded secrets in Node.js applications."""
    
    def __init__(self):
        super().__init__(
            rule_id="nodejs.hardcoded_secrets",
            description="Hardcoded credentials and secrets in Node.js code",
            severity=Severity.CRITICAL,
            category="security"
        )
        self.languages = ['.js', '.ts', '.jsx', '.tsx']
        self.framework = 'nodejs'
    
    def check(self, file_path: Path, parsed_content: Optional[Any] = None) -> List[Issue]:
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            
            # Node.js specific secret patterns
            secret_patterns = [
                (r'(?i)(DB_PASS|DB_PASSWORD|DATABASE_PASSWORD)\s*=\s*[\'"][^\'"]{3,}[\'"]', 
                 "Hardcoded database password", "ISO 27001 A.9.4.3, OWASP A02"),
                (r'(?i)(JWT_SECRET|JWT_KEY)\s*=\s*[\'"][^\'"]{8,}[\'"]', 
                 "Hardcoded JWT secret", "ISO 27001 A.10.1.2, OWASP A02"),
                (r'(?i)(API_KEY|APIKEY)\s*=\s*[\'"][^\'"]{10,}[\'"]', 
                 "Hardcoded API key", "ISO 27001 A.9.4.3, OWASP A02"),
                (r'(?i)(SECRET_KEY|SECRET)\s*=\s*[\'"][^\'"]{8,}[\'"]', 
                 "Hardcoded secret key", "ISO 27001 A.10.1.2, OWASP A02"),
                (r'(?i)(PRIVATE_KEY|PRIV_KEY)\s*=\s*[\'"][^\'"]{20,}[\'"]', 
                 "Hardcoded private key", "ISO 27001 A.10.1.2, OWASP A02"),
                (r'(?i)(AWS_SECRET_ACCESS_KEY)\s*=\s*[\'"][A-Za-z0-9/+=]{40}[\'"]', 
                 "Hardcoded AWS secret", "ISO 27001 A.9.4.3, OWASP A02"),
            ]
            
            for line_num, line in enumerate(lines, 1):
                for pattern, message, standards in secret_patterns:
                    if re.search(pattern, line):
                        issues.append(self.create_issue(
                            file_path=file_path,
                            message=f"Node.js Security: {message}",
                            line_number=line_num,
                            code_snippet=line.strip(),
                            remediation="Use environment variables or secure configuration management. Never commit secrets to source code.",
                            confidence=0.9,
                            metadata={
                                "framework": "nodejs",
                                "cwe": "CWE-798",
                                "iso27001": "A.9.4.3, A.10.1.2",
                                "owasp": "A02-2021",
                                "standards": standards
                            }
                        ))
        
        except Exception:
            pass
        
        return issues

class ExpressSecurityMisconfigurationRule(BaseRule):
    """Detect Express.js security misconfigurations."""
    
    def __init__(self):
        super().__init__(
            rule_id="express.security_misconfiguration",
            description="Express.js security misconfigurations and vulnerabilities",
            severity=Severity.HIGH,
            category="security"
        )
        self.languages = ['.js', '.ts']
        self.framework = 'express'
    
    def check(self, file_path: Path, parsed_content: Optional[Any] = None) -> List[Issue]:
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.splitlines()
            
            # Express security misconfigurations
            security_checks = [
                (r'app\.use\(cors\(\)\)', 
                 "Permissive CORS configuration allows any origin", 
                 "Configure CORS with specific origins. Use: cors({origin: ['https://yourdomain.com']})",
                 "ISO 27001 A.13.1.3, OWASP A05"),
                
                (r'res\.status\(\d+\)\.json\([^)]*stack[^)]*\)', 
                 "Error stack traces exposed to client", 
                 "Remove stack traces from client responses. Log errors server-side only.",
                 "ISO 27001 A.12.4.1, OWASP A09"),
                
                (r'console\.error\([^)]*stack[^)]*\)', 
                 "Stack traces logged to console in production", 
                 "Use proper logging framework and avoid exposing stack traces.",
                 "ISO 27001 A.12.4.1, OWASP A09"),
                
                (r'app\.get\([\'"][^\'"]*/admin[^\'\"]*[\'"][^,]*,\s*\([^)]*\)\s*=>\s*{[^}]*res\.json',
                 "Admin endpoint without authentication middleware", 
                 "Add authentication middleware before sensitive endpoints.",
                 "ISO 27001 A.9.1.2, OWASP A01"),
                
                (r'jwt\.sign\([^,]+,\s*[^,]+\s*\)', 
                 "JWT token without expiration", 
                 "Add expiration to JWT tokens: jwt.sign(payload, secret, {expiresIn: '1h'})",
                 "ISO 27001 A.9.2.6, OWASP A07"),
                
                (r'fs\.appendFileSync\([^,]+,\s*JSON\.stringify\([^)]*req\.body[^)]*\)', 
                 "PII data logged to plaintext file", 
                 "Encrypt sensitive data before logging and implement proper access controls.",
                 "ISO 27001 A.8.2.3, GDPR Art.32"),
                
                (r'res\.json\([^}]*[\'"]?dbPass[\'"]?\s*:', 
                 "Database credentials exposed via API", 
                 "Never expose credentials through API endpoints.",
                 "ISO 27001 A.9.4.3, OWASP A02"),
                
                (r'const\s+q\s*=\s*req\.body\.q[^;]*;\s*[^;]*query[^;]*q', 
                 "Potential SQL injection from unsanitized input", 
                 "Validate and sanitize all user inputs. Use parameterized queries.",
                 "ISO 27001 A.14.2.1, OWASP A03"),
            ]
            
            for line_num, line in enumerate(lines, 1):
                for pattern, message, remediation, standards in security_checks:
                    if re.search(pattern, line, re.IGNORECASE):
                        issues.append(self.create_issue(
                            file_path=file_path,
                            message=f"Express Security: {message}",
                            line_number=line_num,
                            code_snippet=line.strip(),
                            remediation=remediation,
                            confidence=0.8,
                            metadata={
                                "framework": "express",
                                "cwe": "CWE-16",
                                "iso27001": standards.split(", ")[0] if ", " in standards else standards,
                                "owasp": standards.split(", ")[1] if ", " in standards else "",
                                "standards": standards
                            }
                        ))
        
        except Exception:
            pass
        
        return issues

class NodeJSInputValidationRule(BaseRule):
    """Detect missing input validation in Node.js applications."""
    
    def __init__(self):
        super().__init__(
            rule_id="nodejs.input_validation",
            description="Missing input validation and sanitization",
            severity=Severity.HIGH,
            category="security"
        )
        self.languages = ['.js', '.ts']
        self.framework = 'nodejs'
    
    def check(self, file_path: Path, parsed_content: Optional[Any] = None) -> List[Issue]:
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.splitlines()
            
            # Check for routes that use req.body without validation
            route_pattern = r'app\.(get|post|put|delete)\s*\([^,]+,\s*\([^)]*req[^)]*\)\s*=>\s*{'
            body_usage_pattern = r'req\.body\.[a-zA-Z_][a-zA-Z0-9_]*'
            
            in_route = False
            route_start = 0
            
            for line_num, line in enumerate(lines, 1):
                # Check if we're entering a route handler
                if re.search(route_pattern, line):
                    in_route = True
                    route_start = line_num
                    continue
                
                # Check if we're using req.body without validation
                if in_route and re.search(body_usage_pattern, line):
                    # Look for validation patterns in the same route
                    route_end = min(line_num + 10, len(lines))  # Check next 10 lines
                    validation_found = False
                    
                    for check_line in lines[route_start-1:route_end]:
                        if re.search(r'(validate|sanitize|joi\.|yup\.|express-validator)', check_line, re.IGNORECASE):
                            validation_found = True
                            break
                    
                    if not validation_found:
                        issues.append(self.create_issue(
                            file_path=file_path,
                            message="Node.js Security: User input used without validation",
                            line_number=line_num,
                            code_snippet=line.strip(),
                            remediation="Implement input validation using libraries like Joi, Yup, or express-validator",
                            confidence=0.7,
                            metadata={
                                "framework": "nodejs",
                                "cwe": "CWE-20",
                                "iso27001": "A.14.2.1",
                                "owasp": "A03-2021",
                                "asvs": "V5.1.1"
                            }
                        ))
                
                # Reset route tracking on closing brace (simplified)
                if in_route and line.strip() == '});':
                    in_route = False
        
        except Exception:
            pass
        
        return issues

class NodeJSLoggingSecurityRule(BaseRule):
    """Detect insecure logging practices in Node.js."""
    
    def __init__(self):
        super().__init__(
            rule_id="nodejs.logging_security",
            description="Insecure logging practices and PII exposure",
            severity=Severity.MEDIUM,
            category="security"
        )
        self.languages = ['.js', '.ts']
        self.framework = 'nodejs'
    
    def check(self, file_path: Path, parsed_content: Optional[Any] = None) -> List[Issue]:
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            
            logging_checks = [
                (r'console\.log\([^)]*password[^)]*\)', 
                 "Password logged to console", 
                 "Never log passwords or sensitive credentials",
                 "ISO 27001 A.12.4.1, GDPR Art.32"),
                
                (r'console\.log\([^)]*token[^)]*\)', 
                 "Authentication token logged to console", 
                 "Avoid logging authentication tokens",
                 "ISO 27001 A.12.4.1, OWASP A09"),
                
                (r'fs\.appendFileSync\([^,]+,\s*[^)]*req\.body[^)]*\)', 
                 "Request body logged to file without encryption", 
                 "Encrypt sensitive data before logging and implement access controls",
                 "ISO 27001 A.8.2.3, GDPR Art.32"),
                
                (r'console\.error\([^)]*err\.stack[^)]*\)', 
                 "Full error stack traces logged", 
                 "Log error details securely, avoid exposing stack traces in production",
                 "ISO 27001 A.12.4.1, OWASP A09"),
                
                (r'res\.json\([^}]*stack[^}]*\)', 
                 "Error stack trace returned to client", 
                 "Never return stack traces to clients in production",
                 "ISO 27001 A.12.4.1, OWASP A09"),
            ]
            
            for line_num, line in enumerate(lines, 1):
                for pattern, message, remediation, standards in logging_checks:
                    if re.search(pattern, line, re.IGNORECASE):
                        issues.append(self.create_issue(
                            file_path=file_path,
                            message=f"Node.js Logging: {message}",
                            line_number=line_num,
                            code_snippet=line.strip(),
                            remediation=remediation,
                            confidence=0.8,
                            metadata={
                                "framework": "nodejs",
                                "cwe": "CWE-532",
                                "iso27001": "A.12.4.1",
                                "gdpr": "Art.32" if "GDPR" in standards else "",
                                "owasp": "A09-2021",
                                "standards": standards
                            }
                        ))
        
        except Exception:
            pass
        
        return issues

class NodeJSAuthenticationRule(BaseRule):
    """Detect authentication and authorization issues in Node.js."""
    
    def __init__(self):
        super().__init__(
            rule_id="nodejs.authentication",
            description="Authentication and authorization security issues",
            severity=Severity.HIGH,
            category="security"
        )
        self.languages = ['.js', '.ts']
        self.framework = 'nodejs'
    
    def check(self, file_path: Path, parsed_content: Optional[Any] = None) -> List[Issue]:
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.splitlines()
            
            auth_checks = [
                (r'if\s*\(\s*username\s*===\s*[\'"][^\'"]+[\'"]\s*&&\s*password\s*===\s*[\'"][^\'"]+[\'"]\s*\)', 
                 "Hardcoded authentication credentials", 
                 "Use secure authentication with hashed passwords and proper user management",
                 "ISO 27001 A.9.2.1, OWASP A07"),
                
                (r'app\.(get|post|put|delete)\s*\([\'"][^\'"]*admin[^\'\"]*[\'"][^,]*,\s*\([^)]*\)\s*=>\s*{(?![^}]*auth)',
                 "Admin endpoint without authentication middleware", 
                 "Implement authentication middleware for all admin endpoints",
                 "ISO 27001 A.9.1.2, OWASP A01"),
                
                (r'jwt\.sign\([^,]+,\s*[^,]+\s*\)(?![^;]*expiresIn)', 
                 "JWT token without expiration time", 
                 "Always set expiration time for JWT tokens to limit exposure",
                 "ISO 27001 A.9.2.6, OWASP A07"),
                
                (r'res\.json\([^}]*(?:password|secret|key)[^}]*\)', 
                 "Sensitive data exposed in API response", 
                 "Never include sensitive data in API responses",
                 "ISO 27001 A.9.4.3, OWASP A02"),
            ]
            
            for line_num, line in enumerate(lines, 1):
                for pattern, message, remediation, standards in auth_checks:
                    if re.search(pattern, line, re.IGNORECASE):
                        issues.append(self.create_issue(
                            file_path=file_path,
                            message=f"Node.js Authentication: {message}",
                            line_number=line_num,
                            code_snippet=line.strip(),
                            remediation=remediation,
                            confidence=0.8,
                            metadata={
                                "framework": "nodejs",
                                "cwe": "CWE-287",
                                "iso27001": "A.9.2.1",
                                "owasp": "A07-2021",
                                "asvs": "V2.1.1",
                                "standards": standards
                            }
                        ))
        
        except Exception:
            pass
        
        return issues

class NodeJSRules:
    """Collection of comprehensive Node.js security rules."""
    
    @staticmethod
    def get_rules() -> List[BaseRule]:
        """Get all Node.js security rules."""
        return [
            NodeJSHardcodedSecretsRule(),
            ExpressSecurityMisconfigurationRule(),
            NodeJSInputValidationRule(),
            NodeJSLoggingSecurityRule(),
            NodeJSAuthenticationRule(),
        ]