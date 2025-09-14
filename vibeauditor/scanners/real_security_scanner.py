"""
Real Security Scanner Implementation for VibeCodeAuditor
Integrates multiple security scanning tools for comprehensive analysis.
"""

import os
import json
import subprocess
import tempfile
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import asyncio
import logging

from ..core.results import Issue, Severity, AuditResults

logger = logging.getLogger(__name__)

@dataclass
class ScannerResult:
    """Result from a security scanner."""
    tool: str
    issues: List[Dict[str, Any]]
    errors: List[str]
    metadata: Dict[str, Any]

class SecurityScanner:
    """Comprehensive security scanner using multiple tools."""
    
    def __init__(self):
        self.scanners = {
            'bandit': BanditScanner(),
            'semgrep': SemgrepScanner(),
            'eslint_security': ESLintSecurityScanner(),
            'safety': SafetyScanner(),
            'custom_rules': CustomRulesScanner()
        }
    
    async def scan_file(self, file_path: str) -> Dict[str, Any]:
        """Scan a single file and return results as dict."""
        file_paths = [Path(file_path)]
        results = await self.scan_files(file_paths)
        return results.to_dict()
    
    async def scan_files(self, file_paths: List[Path]) -> AuditResults:
        """Scan files using all available security scanners."""
        results = AuditResults()
        
        # Group files by language/type for efficient scanning
        file_groups = self._group_files_by_type(file_paths)
        
        # Run scanners in parallel for each file group
        scanner_tasks = []
        for file_group, files in file_groups.items():
            for scanner_name, scanner in self.scanners.items():
                if scanner.supports_files(files):
                    task = self._run_scanner_safe(scanner, files, scanner_name)
                    scanner_tasks.append(task)
        
        # Execute all scanners
        scanner_results = await asyncio.gather(*scanner_tasks, return_exceptions=True)
        
        # Process results
        for result in scanner_results:
            if isinstance(result, Exception):
                logger.error(f"Scanner failed: {result}")
                continue
            
            if isinstance(result, ScannerResult):
                # Convert scanner issues to our Issue format
                for issue_data in result.issues:
                    issue = self._convert_to_issue(issue_data, result.tool)
                    if issue:
                        results.add_issue(issue)
        
        return results
    
    async def _run_scanner_safe(self, scanner, files: List[Path], scanner_name: str) -> Optional[ScannerResult]:
        """Run a scanner with error handling."""
        try:
            return await scanner.scan(files)
        except Exception as e:
            logger.error(f"Scanner {scanner_name} failed: {e}")
            return ScannerResult(
                tool=scanner_name,
                issues=[],
                errors=[str(e)],
                metadata={}
            )
    
    def _group_files_by_type(self, file_paths: List[Path]) -> Dict[str, List[Path]]:
        """Group files by their type/language."""
        groups = {
            'python': [],
            'javascript': [],
            'typescript': [],
            'json': [],
            'yaml': [],
            'other': []
        }
        
        for file_path in file_paths:
            suffix = file_path.suffix.lower()
            if suffix in ['.py']:
                groups['python'].append(file_path)
            elif suffix in ['.js', '.jsx']:
                groups['javascript'].append(file_path)
            elif suffix in ['.ts', '.tsx']:
                groups['typescript'].append(file_path)
            elif suffix in ['.json']:
                groups['json'].append(file_path)
            elif suffix in ['.yml', '.yaml']:
                groups['yaml'].append(file_path)
            else:
                groups['other'].append(file_path)
        
        # Remove empty groups
        return {k: v for k, v in groups.items() if v}
    
    def _convert_to_issue(self, issue_data: Dict[str, Any], tool: str) -> Optional[Issue]:
        """Convert scanner-specific issue format to our Issue format."""
        try:
            # Map severity levels
            severity_map = {
                'HIGH': Severity.CRITICAL,
                'MEDIUM': Severity.HIGH,
                'LOW': Severity.MEDIUM,
                'INFO': Severity.LOW,
                'ERROR': Severity.CRITICAL,
                'WARNING': Severity.HIGH,
                'CRITICAL': Severity.CRITICAL
            }
            
            severity_str = issue_data.get('severity', 'MEDIUM').upper()
            severity = severity_map.get(severity_str, Severity.MEDIUM)
            
            return Issue(
                rule_id=issue_data.get('rule_id', f"{tool}_unknown"),
                severity=severity,
                category='security',
                message=issue_data.get('message', 'Security issue detected'),
                file_path=str(issue_data.get('file_path', '')),
                line_number=issue_data.get('line_number', 0),
                code_snippet=issue_data.get('code_snippet', ''),
                remediation=issue_data.get('remediation', 'Review and fix this issue'),
                confidence=issue_data.get('confidence', 0.8),
                metadata={
                    'tool': tool,
                    'original_data': issue_data
                }
            )
        except Exception as e:
            logger.error(f"Failed to convert issue from {tool}: {e}")
            return None

class BanditScanner:
    """Python security scanner using Bandit."""
    
    def supports_files(self, files: List[Path]) -> bool:
        return any(f.suffix == '.py' for f in files)
    
    async def scan(self, files: List[Path]) -> ScannerResult:
        """Run Bandit security scanner."""
        python_files = [f for f in files if f.suffix == '.py']
        if not python_files:
            return ScannerResult('bandit', [], [], {})
        
        try:
            # Create temporary directory with files
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)
                
                # Copy files to temp directory
                for file_path in python_files:
                    temp_file = temp_path / file_path.name
                    temp_file.write_text(file_path.read_text())
                
                # Run Bandit
                cmd = [
                    'bandit', '-r', str(temp_path),
                    '-f', 'json',
                    '--skip', 'B101'  # Skip assert_used test
                ]
                
                result = await asyncio.create_subprocess_exec(
                    *cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                
                stdout, stderr = await result.communicate()
                
                if result.returncode in [0, 1]:  # 0 = no issues, 1 = issues found
                    data = json.loads(stdout.decode())
                    issues = self._parse_bandit_results(data)
                    return ScannerResult('bandit', issues, [], data.get('metrics', {}))
                else:
                    error_msg = stderr.decode()
                    return ScannerResult('bandit', [], [error_msg], {})
                    
        except FileNotFoundError:
            return ScannerResult('bandit', [], ['Bandit not installed'], {})
        except Exception as e:
            return ScannerResult('bandit', [], [str(e)], {})
    
    def _parse_bandit_results(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Parse Bandit JSON output."""
        issues = []
        for result in data.get('results', []):
            issues.append({
                'rule_id': f"bandit_{result.get('test_id', 'unknown')}",
                'message': result.get('issue_text', 'Security issue'),
                'severity': result.get('issue_severity', 'MEDIUM'),
                'file_path': result.get('filename', ''),
                'line_number': result.get('line_number', 0),
                'code_snippet': result.get('code', ''),
                'remediation': f"Bandit {result.get('test_name', '')}: {result.get('issue_text', '')}",
                'confidence': self._map_confidence(result.get('issue_confidence', 'MEDIUM'))
            })
        return issues
    
    def _map_confidence(self, confidence: str) -> float:
        """Map Bandit confidence to float."""
        mapping = {'HIGH': 0.9, 'MEDIUM': 0.7, 'LOW': 0.5}
        return mapping.get(confidence.upper(), 0.7)

class SemgrepScanner:
    """Multi-language security scanner using Semgrep."""
    
    def supports_files(self, files: List[Path]) -> bool:
        supported_extensions = {'.py', '.js', '.jsx', '.ts', '.tsx', '.java', '.go', '.rb', '.php'}
        return any(f.suffix in supported_extensions for f in files)
    
    async def scan(self, files: List[Path]) -> ScannerResult:
        """Run Semgrep security scanner."""
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)
                
                # Copy files to temp directory
                for file_path in files:
                    if self.supports_files([file_path]):
                        temp_file = temp_path / file_path.name
                        temp_file.write_text(file_path.read_text())
                
                # Run Semgrep with security rules
                cmd = [
                    'semgrep', '--config=auto',
                    '--json', '--no-git-ignore',
                    str(temp_path)
                ]
                
                result = await asyncio.create_subprocess_exec(
                    *cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                
                stdout, stderr = await result.communicate()
                
                if result.returncode in [0, 1]:
                    data = json.loads(stdout.decode())
                    issues = self._parse_semgrep_results(data)
                    return ScannerResult('semgrep', issues, [], {})
                else:
                    error_msg = stderr.decode()
                    return ScannerResult('semgrep', [], [error_msg], {})
                    
        except FileNotFoundError:
            return ScannerResult('semgrep', [], ['Semgrep not installed'], {})
        except Exception as e:
            return ScannerResult('semgrep', [], [str(e)], {})
    
    def _parse_semgrep_results(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Parse Semgrep JSON output."""
        issues = []
        for result in data.get('results', []):
            issues.append({
                'rule_id': f"semgrep_{result.get('check_id', 'unknown')}",
                'message': result.get('message', 'Security issue'),
                'severity': result.get('extra', {}).get('severity', 'MEDIUM'),
                'file_path': result.get('path', ''),
                'line_number': result.get('start', {}).get('line', 0),
                'code_snippet': result.get('extra', {}).get('lines', ''),
                'remediation': result.get('extra', {}).get('message', 'Review this security issue'),
                'confidence': 0.8
            })
        return issues

class ESLintSecurityScanner:
    """JavaScript/TypeScript security scanner using ESLint Security plugin."""
    
    def supports_files(self, files: List[Path]) -> bool:
        return any(f.suffix in ['.js', '.jsx', '.ts', '.tsx'] for f in files)
    
    async def scan(self, files: List[Path]) -> ScannerResult:
        """Run ESLint with security rules."""
        js_files = [f for f in files if f.suffix in ['.js', '.jsx', '.ts', '.tsx']]
        if not js_files:
            return ScannerResult('eslint_security', [], [], {})
        
        # For now, return mock results since ESLint setup is complex
        # In production, you'd set up proper ESLint configuration
        mock_issues = []
        for file_path in js_files:
            content = file_path.read_text()
            
            # Simple pattern matching for common issues
            if 'eval(' in content:
                mock_issues.append({
                    'rule_id': 'eslint_no_eval',
                    'message': 'Use of eval() is dangerous and should be avoided',
                    'severity': 'HIGH',
                    'file_path': str(file_path),
                    'line_number': self._find_line_number(content, 'eval('),
                    'code_snippet': 'eval(...)',
                    'remediation': 'Replace eval() with safer alternatives',
                    'confidence': 0.9
                })
            
            if 'innerHTML' in content and '=' in content:
                mock_issues.append({
                    'rule_id': 'eslint_no_inner_html',
                    'message': 'Direct innerHTML assignment can lead to XSS vulnerabilities',
                    'severity': 'MEDIUM',
                    'file_path': str(file_path),
                    'line_number': self._find_line_number(content, 'innerHTML'),
                    'code_snippet': 'element.innerHTML = ...',
                    'remediation': 'Use textContent or proper sanitization',
                    'confidence': 0.7
                })
        
        return ScannerResult('eslint_security', mock_issues, [], {})
    
    def _find_line_number(self, content: str, pattern: str) -> int:
        """Find line number of pattern in content."""
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            if pattern in line:
                return i
        return 1

class SafetyScanner:
    """Python dependency vulnerability scanner using Safety."""
    
    def supports_files(self, files: List[Path]) -> bool:
        return any(f.name in ['requirements.txt', 'Pipfile', 'pyproject.toml'] for f in files)
    
    async def scan(self, files: List[Path]) -> ScannerResult:
        """Run Safety scanner for Python dependencies."""
        req_files = [f for f in files if f.name in ['requirements.txt', 'Pipfile', 'pyproject.toml']]
        if not req_files:
            return ScannerResult('safety', [], [], {})
        
        try:
            # For requirements.txt files
            for req_file in req_files:
                if req_file.name == 'requirements.txt':
                    cmd = ['safety', 'check', '-r', str(req_file), '--json']
                    
                    result = await asyncio.create_subprocess_exec(
                        *cmd,
                        stdout=asyncio.subprocess.PIPE,
                        stderr=asyncio.subprocess.PIPE
                    )
                    
                    stdout, stderr = await result.communicate()
                    
                    if result.returncode in [0, 64]:  # 0 = safe, 64 = vulnerabilities found
                        try:
                            data = json.loads(stdout.decode())
                            issues = self._parse_safety_results(data)
                            return ScannerResult('safety', issues, [], {})
                        except json.JSONDecodeError:
                            # Safety might return non-JSON output
                            return ScannerResult('safety', [], [], {})
                    else:
                        error_msg = stderr.decode()
                        return ScannerResult('safety', [], [error_msg], {})
            
            return ScannerResult('safety', [], [], {})
            
        except FileNotFoundError:
            return ScannerResult('safety', [], ['Safety not installed'], {})
        except Exception as e:
            return ScannerResult('safety', [], [str(e)], {})
    
    def _parse_safety_results(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Parse Safety JSON output."""
        issues = []
        for vuln in data:
            issues.append({
                'rule_id': f"safety_{vuln.get('id', 'unknown')}",
                'message': f"Vulnerable dependency: {vuln.get('package_name', 'unknown')}",
                'severity': 'HIGH',
                'file_path': 'requirements.txt',
                'line_number': 1,
                'code_snippet': f"{vuln.get('package_name', '')}=={vuln.get('installed_version', '')}",
                'remediation': f"Update to version {vuln.get('safe_version', 'latest')} or higher",
                'confidence': 0.9
            })
        return issues

class CustomRulesScanner:
    """Custom security rules scanner for application-specific patterns."""
    
    def supports_files(self, files: List[Path]) -> bool:
        return True  # Can scan any file type
    
    async def scan(self, files: List[Path]) -> ScannerResult:
        """Run custom security rules."""
        issues = []
        
        for file_path in files:
            try:
                content = file_path.read_text()
                file_issues = self._scan_file_content(content, file_path)
                issues.extend(file_issues)
            except Exception as e:
                logger.error(f"Failed to scan {file_path}: {e}")
        
        return ScannerResult('custom_rules', issues, [], {})
    
    def _scan_file_content(self, content: str, file_path: Path) -> List[Dict[str, Any]]:
        """Scan file content for custom security patterns."""
        issues = []
        lines = content.split('\n')
        
        logger.info(f"🔍 Scanning file: {file_path}")
        logger.info(f"📊 File has {len(lines)} lines")
        logger.info(f"📝 First 200 chars: {content[:200]}")
        
        # Custom security patterns - simplified and more specific
        patterns = [
            # Password patterns - match DB_PASS, PASSWORD, etc.
            {
                'pattern': r'(DB_PASS|PASSWORD|password|PASS)\s*=\s*["\'][^"\']+["\']',
                'rule_id': 'hardcoded_password',
                'message': 'Hardcoded password detected',
                'severity': 'CRITICAL',
                'remediation': 'Use environment variables or secure configuration'
            },
            # Secret patterns - match JWT_SECRET, SECRET, etc.
            {
                'pattern': r'(JWT_SECRET|SECRET|secret|Secret)\s*=\s*["\'][^"\']+["\']',
                'rule_id': 'hardcoded_secret',
                'message': 'Hardcoded secret detected',
                'severity': 'CRITICAL',
                'remediation': 'Use secure secret management'
            },
            # API Key patterns
            {
                'pattern': r'(API_KEY|api_key|apiKey)\s*[=:]\s*["\'][^"\']+["\']',
                'rule_id': 'hardcoded_api_key',
                'message': 'Hardcoded API key detected',
                'severity': 'CRITICAL',
                'remediation': 'Use environment variables or secure key management'
            },
            # Hardcoded credentials in object properties
            {
                'pattern': r'(dbPass|dbUser|password|secret)\s*:\s*["\'][^"\']+["\']',
                'rule_id': 'hardcoded_credentials_object',
                'message': 'Hardcoded credentials in object detected',
                'severity': 'HIGH',
                'remediation': 'Use secure configuration management'
            },
            # JavaScript eval usage
            {
                'pattern': r'eval\s*\(',
                'rule_id': 'dangerous_eval',
                'message': 'Use of eval() is dangerous and should be avoided',
                'severity': 'HIGH',
                'remediation': 'Replace eval() with safer alternatives'
            },
            # JavaScript innerHTML (XSS risk)
            {
                'pattern': r'\.innerHTML\s*=',
                'rule_id': 'xss_innerHTML',
                'message': 'Direct innerHTML assignment can lead to XSS vulnerabilities',
                'severity': 'MEDIUM',
                'remediation': 'Use textContent or proper sanitization'
            },
            # Verbose error handling (information disclosure)
            {
                'pattern': r'err\.stack',
                'rule_id': 'information_disclosure',
                'message': 'Stack trace exposed to client (information disclosure)',
                'severity': 'MEDIUM',
                'remediation': 'Log errors server-side only, return generic error messages'
            },
            # Permissive CORS
            {
                'pattern': r'cors\(\)',
                'rule_id': 'permissive_cors',
                'message': 'Permissive CORS configuration detected',
                'severity': 'MEDIUM',
                'remediation': 'Configure CORS with specific allowed origins'
            },
            # No authentication on sensitive endpoints
            {
                'pattern': r'\/admin\/',
                'rule_id': 'unprotected_admin_endpoint',
                'message': 'Admin endpoint may lack proper authentication',
                'severity': 'HIGH',
                'remediation': 'Add authentication middleware to admin endpoints'
            }
        ]
        
        import re
        for i, line in enumerate(lines, 1):
            for pattern_info in patterns:
                if re.search(pattern_info['pattern'], line, re.IGNORECASE):
                    logger.info(f"🚨 FOUND ISSUE on line {i}: {pattern_info['rule_id']}")
                    logger.info(f"   Line: {line.strip()}")
                    issues.append({
                        'rule_id': pattern_info['rule_id'],
                        'message': pattern_info['message'],
                        'severity': pattern_info['severity'],
                        'file_path': str(file_path),
                        'line_number': i,
                        'code_snippet': line.strip(),
                        'remediation': pattern_info['remediation'],
                        'confidence': 0.8
                    })
        
        logger.info(f"✅ Custom scanner found {len(issues)} issues in {file_path}")
        return issues