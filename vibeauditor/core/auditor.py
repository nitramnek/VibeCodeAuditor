"""
Main auditing engine for VibeCodeAuditor.
"""

from pathlib import Path
from typing import List, Dict, Any
from rich.progress import Progress, TaskID

from .config import AuditorConfig
from .results import AuditResults, Issue
from .framework_detector import FrameworkDetector
from .standards_mapper import StandardsMapper
from ..scanners import get_scanner_for_file
from ..rules import get_enabled_rules
from ..rules.framework_rules import FrameworkRules

class CodeAuditor:
    """Main code auditing engine with framework-aware analysis."""
    
    def __init__(self, config: AuditorConfig):
        self.config = config
        self.framework_detector = FrameworkDetector()
        self.standards_mapper = StandardsMapper()
        self.detected_frameworks = {}
        self.rules = get_enabled_rules(config)
    
    def scan(self, target_path: Path) -> AuditResults:
        """Scan a directory or file for issues with framework-aware analysis."""
        results = AuditResults()
        
        # First, detect frameworks in the codebase
        print("🔍 Detecting frameworks...")
        self.detected_frameworks = self.framework_detector.detect_frameworks(target_path)
        
        if self.detected_frameworks:
            print(f"📋 Detected frameworks: {', '.join(self.detected_frameworks.keys())}")
            # Add framework-specific rules
            framework_rules = FrameworkRules.get_rules_for_frameworks(self.detected_frameworks)
            self.rules.extend(framework_rules)
            print(f"✅ Added {len(framework_rules)} framework-specific rules")
        else:
            print("📋 No specific frameworks detected, using general rules")
        
        # Store framework information in results
        results.detected_frameworks = self.detected_frameworks
        
        if target_path.is_file():
            files_to_scan = [target_path]
        else:
            files_to_scan = self._get_files_to_scan(target_path)
        
        with Progress() as progress:
            task = progress.add_task("Scanning files...", total=len(files_to_scan))
            
            for file_path in files_to_scan:
                try:
                    file_issues = self._scan_file(file_path)
                    results.add_issues(file_issues)
                except Exception as e:
                    results.add_error(file_path, str(e))
                
                progress.update(task, advance=1)
        
        # Enhance issues with standards mapping
        self._enhance_issues_with_standards(results)
        
        return results
    
    def _get_files_to_scan(self, directory: Path) -> List[Path]:
        """Get list of files to scan in directory."""
        files = []
        
        for file_path in directory.rglob("*"):
            if file_path.is_file() and self.config.should_scan_file(file_path):
                files.append(file_path)
        
        return files
    
    def _scan_file(self, file_path: Path) -> List[Issue]:
        """Scan a single file for issues."""
        issues = []
        
        # Get appropriate scanner for file type
        scanner = get_scanner_for_file(file_path)
        if not scanner:
            return issues
        
        # Parse file
        try:
            parsed_content = scanner.parse_file(file_path)
        except Exception:
            # If parsing fails, skip advanced analysis
            parsed_content = None
        
        # Apply rules
        for rule in self.rules:
            if rule.applies_to_file(file_path):
                try:
                    rule_issues = rule.check(file_path, parsed_content)
                    issues.extend(rule_issues)
                except Exception as e:
                    # Log rule execution error but continue
                    pass
        
        # Limit issues per file
        if len(issues) > self.config.max_issues_per_file:
            issues = issues[:self.config.max_issues_per_file]
        
        return issues
    
    def _enhance_issues_with_standards(self, results: AuditResults):
        """Enhance issues with standards and compliance information."""
        print("📋 Mapping issues to industry standards...")
        
        for issue in results.issues:
            # Get framework context
            framework = None
            if hasattr(issue, 'metadata') and issue.metadata:
                framework = issue.metadata.get('framework')
            
            # Map to standards
            standards = self.standards_mapper.get_standards_for_issue(
                rule_id=issue.rule_id,
                cwe_id=issue.metadata.get('cwe') if issue.metadata else None,
                category=issue.category,
                framework=framework
            )
            
            # Update issue with standards
            issue.standards = standards
            
            # Extract compliance frameworks (both compliance and security standards)
            compliance_frameworks = []
            for std in standards:
                if std.type.value == 'compliance':
                    # Extract framework name from full standard name
                    if 'GDPR' in std.name:
                        compliance_frameworks.append('GDPR')
                    elif 'PCI DSS' in std.name:
                        compliance_frameworks.append('PCI DSS')
                    elif 'HIPAA' in std.name:
                        compliance_frameworks.append('HIPAA')
                    elif 'SOX' in std.name:
                        compliance_frameworks.append('SOX')
                elif std.type.value == 'security':
                    # Include major security standards as compliance frameworks
                    if 'OWASP' in std.name:
                        compliance_frameworks.append('OWASP')
                    elif 'ISO' in std.name:
                        compliance_frameworks.append('ISO 27001')
                    elif 'NIST' in std.name:
                        compliance_frameworks.append('NIST')
            
            # Remove duplicates and store
            issue.compliance_frameworks = list(set(compliance_frameworks))
        
        # Store compliance summary in results
        results.compliance_summary = self.standards_mapper.get_compliance_summary(results.issues)
        print(f"✅ Mapped {len(results.issues)} issues to industry standards")