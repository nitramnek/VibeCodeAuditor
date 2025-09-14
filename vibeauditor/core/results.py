"""
Results and data structures for VibeCodeAuditor.
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from pathlib import Path
import json

class Severity(Enum):
    """Issue severity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class Issue:
    """Represents a security issue found during scanning."""
    rule_id: str
    severity: Severity
    category: str
    message: str
    file_path: str  # Changed from Path to str for simplicity
    line_number: int = 0
    code_snippet: str = ""
    remediation: str = ""
    confidence: float = 0.8
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert issue to dictionary."""
        return {
            "rule_id": self.rule_id,
            "severity": self.severity.value,
            "category": self.category,
            "message": self.message,
            "file_path": self.file_path,
            "line_number": self.line_number,
            "code_snippet": self.code_snippet,
            "remediation": self.remediation,
            "confidence": self.confidence,
            "metadata": self.metadata
        }

@dataclass
class AuditResults:
    """Container for audit results."""
    issues: List[Issue] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def add_issue(self, issue: Issue):
        """Add an issue to the results."""
        self.issues.append(issue)
    
    def get_issues_by_severity(self, severity: Severity) -> List[Issue]:
        """Get issues filtered by severity."""
        return [issue for issue in self.issues if issue.severity == severity]
    
    def get_severity_counts(self) -> Dict[str, int]:
        """Get count of issues by severity."""
        counts = {severity.value: 0 for severity in Severity}
        for issue in self.issues:
            counts[issue.severity.value] += 1
        return counts
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert results to dictionary."""
        return {
            "issues": [issue.to_dict() for issue in self.issues],
            "summary": {
                "total_issues": len(self.issues),
                "severity_counts": self.get_severity_counts()
            },
            "metadata": self.metadata
        }
    
    def to_json(self) -> str:
        """Convert results to JSON string."""
        return json.dumps(self.to_dict(), indent=2)