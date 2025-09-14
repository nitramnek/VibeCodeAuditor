"""
Base rule class for audit rules.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Optional, Any
from ..core.results import Issue, Severity

class BaseRule(ABC):
    """Base class for all audit rules."""
    
    def __init__(self, rule_id: str, description: str, severity: Severity, category: str = "general"):
        self.id = rule_id
        self.description = description
        self.severity = severity
        self.category = category
        self.languages = []  # Override in subclasses
        self.tags = []
    
    @abstractmethod
    def check(self, file_path: Path, parsed_content: Optional[Any] = None) -> List[Issue]:
        """Check file for rule violations."""
        pass
    
    def applies_to_file(self, file_path: Path) -> bool:
        """Check if rule applies to given file."""
        if not self.languages:
            return True
        
        suffix = file_path.suffix.lower()
        return suffix in self.languages
    
    def create_issue(
        self,
        file_path: Path,
        message: str,
        line_number: Optional[int] = None,
        column_number: Optional[int] = None,
        code_snippet: Optional[str] = None,
        remediation: Optional[str] = None,
        confidence: float = 1.0,
        metadata: Optional[dict] = None
    ) -> Issue:
        """Helper to create an issue."""
        return Issue(
            rule_id=self.id,
            severity=self.severity,
            message=message,
            file_path=file_path,
            line_number=line_number,
            column_number=column_number,
            code_snippet=code_snippet,
            remediation=remediation,
            category=self.category,
            confidence=confidence,
            metadata=metadata or {}
        )