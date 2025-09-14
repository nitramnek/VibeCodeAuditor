"""
Security-focused audit rules.
"""

import re
from pathlib import Path
from typing import List, Optional, Any

from .base_rule import BaseRule
from ..core.results import Issue, Severity

class HardcodedSecretsRule(BaseRule):
    """Detect hardcoded secrets and credentials."""
    
    def __init__(self):
        super().__init__(
            rule_id="security.hardcoded_secrets",
            description="Detects hardcoded secrets, API keys, and credentials",
            severity=Severity.HIGH,
            category="security"
        )
        
        # Common secret patterns
        self.secret_patterns = [
            (r'(?i)(api[_-]?key|apikey)\s*[=:]\s*["\']([a-zA-Z0-9_-]{20,})["\']', "API Key"),
            (r'(?i)(secret[_-]?key|secretkey)\s*[=:]\s*["\']([a-zA-Z0-9_-]{20,})["\']', "Secret Key"),
            (r'(?i)(password|pwd)\s*[=:]\s*["\']([^"\']{8,})["\']', "Password"),
            (r'(?i)(token)\s*[=:]\s*["\']([a-zA-Z0-9_-]{20,})["\']', "Token"),
            (r'(?i)(aws[_-]?access[_-]?key[_-]?id)\s*[=:]\s*["\']([A-Z0-9]{20})["\']', "AWS Access Key"),
            (r'(?i)(aws[_-]?secret[_-]?access[_-]?key)\s*[=:]\s*["\']([a-zA-Z0-9/+=]{40})["\']', "AWS Secret Key"),
        ]
    
    def check(self, file_path: Path, parsed_content: Optional[Any] = None) -> List[Issue]:
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            
            for line_num, line in enumerate(lines, 1):
                for pattern, secret_type in self.secret_patterns:
                    matches = re.finditer(pattern, line)
                    for match in matches:
                        # Skip obvious test/example values
                        value = match.group(2) if len(match.groups()) > 1 else match.group(1)
                        if self._is_likely_real_secret(value):
                            issues.append(self.create_issue(
                                file_path=file_path,
                                message=f"Potential hardcoded {secret_type.lower()} detected",
                                line_number=line_num,
                                code_snippet=line.strip(),
                                remediation=f"Move {secret_type.lower()} to environment variables or secure configuration",
                                confidence=0.8,
                                metadata={"secret_type": secret_type}
                            ))
        
        except Exception:
            pass
        
        return issues
    
    def _is_likely_real_secret(self, value: str) -> bool:
        """Check if value looks like a real secret (not test/placeholder)."""
        test_indicators = [
            'test', 'example', 'demo', 'placeholder', 'your_key_here',
            'xxx', '123', 'abc', 'fake', 'dummy', 'sample'
        ]
        
        value_lower = value.lower()
        return not any(indicator in value_lower for indicator in test_indicators)

class SQLInjectionRule(BaseRule):
    """Detect potential SQL injection vulnerabilities."""
    
    def __init__(self):
        super().__init__(
            rule_id="security.sql_injection",
            description="Detects potential SQL injection vulnerabilities",
            severity=Severity.HIGH,
            category="security"
        )
        self.languages = ['.py', '.js', '.ts', '.java']
    
    def check(self, file_path: Path, parsed_content: Optional[Any] = None) -> List[Issue]:
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            
            # Patterns for SQL injection vulnerabilities
            sql_patterns = [
                r'(?i)(execute|query|exec)\s*\(\s*["\'].*%s.*["\']',  # String formatting in SQL
                r'(?i)(execute|query|exec)\s*\(\s*.*\+.*\)',  # String concatenation
                r'(?i)f["\'].*select.*{.*}.*["\']',  # f-string with SQL
            ]
            
            for line_num, line in enumerate(lines, 1):
                for pattern in sql_patterns:
                    if re.search(pattern, line):
                        issues.append(self.create_issue(
                            file_path=file_path,
                            message="Potential SQL injection vulnerability detected",
                            line_number=line_num,
                            code_snippet=line.strip(),
                            remediation="Use parameterized queries or prepared statements",
                            confidence=0.7
                        ))
        
        except Exception:
            pass
        
        return issues

class InsecureRandomRule(BaseRule):
    """Detect use of insecure random number generators."""
    
    def __init__(self):
        super().__init__(
            rule_id="security.insecure_random",
            description="Detects use of insecure random number generators",
            severity=Severity.MEDIUM,
            category="security"
        )
        self.languages = ['.py', '.js', '.ts']
    
    def check(self, file_path: Path, parsed_content: Optional[Any] = None) -> List[Issue]:
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.splitlines()
            
            # Check for insecure random usage
            insecure_patterns = [
                (r'import random\b', "Python's random module is not cryptographically secure"),
                (r'Math\.random\(\)', "JavaScript's Math.random() is not cryptographically secure"),
                (r'random\.random\(\)', "random.random() is not cryptographically secure"),
            ]
            
            for line_num, line in enumerate(lines, 1):
                for pattern, message in insecure_patterns:
                    if re.search(pattern, line):
                        issues.append(self.create_issue(
                            file_path=file_path,
                            message=f"Insecure random number generator: {message}",
                            line_number=line_num,
                            code_snippet=line.strip(),
                            remediation="Use cryptographically secure random generators (e.g., secrets module in Python, crypto.getRandomValues() in JavaScript)",
                            confidence=0.9
                        ))
        
        except Exception:
            pass
        
        return issues

class SecurityRules:
    """Collection of security rules."""
    
    @staticmethod
    def get_rules() -> List[BaseRule]:
        """Get all security rules."""
        return [
            HardcodedSecretsRule(),
            SQLInjectionRule(),
            InsecureRandomRule(),
        ]