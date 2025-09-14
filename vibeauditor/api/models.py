"""
Pydantic models for API requests and responses.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

from ..core.results import Issue, Severity, AuditResults
from ..core.config import AuditorConfig

class SeverityModel(str, Enum):
    """Severity levels for API."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class StandardModel(BaseModel):
    """API model for standards reference."""
    id: str
    name: str
    type: str
    url: str
    section: Optional[str] = None

class IssueModel(BaseModel):
    """API model for audit issues."""
    rule_id: str
    severity: SeverityModel
    message: str
    file_path: str
    line_number: Optional[int] = None
    column_number: Optional[int] = None
    code_snippet: Optional[str] = None
    remediation: Optional[str] = None
    category: str = "general"
    confidence: float = 1.0
    metadata: Dict[str, Any] = {}
    standards: List[StandardModel] = []
    compliance_frameworks: List[str] = []
    
    @classmethod
    def from_issue(cls, issue: Issue) -> 'IssueModel':
        """Convert core Issue to API model."""
        standards = []
        if hasattr(issue, 'standards') and issue.standards:
            standards = [
                StandardModel(
                    id=std.id,
                    name=std.name,
                    type=std.type.value,
                    url=std.url,
                    section=std.section
                ) for std in issue.standards
            ]
        
        compliance_frameworks = []
        if hasattr(issue, 'compliance_frameworks') and issue.compliance_frameworks:
            compliance_frameworks = issue.compliance_frameworks
        
        return cls(
            rule_id=issue.rule_id,
            severity=SeverityModel(issue.severity.value),
            message=issue.message,
            file_path=str(issue.file_path),
            line_number=issue.line_number,
            column_number=issue.column_number,
            code_snippet=issue.code_snippet,
            remediation=issue.remediation,
            category=issue.category,
            confidence=issue.confidence,
            metadata=issue.metadata or {},
            standards=standards,
            compliance_frameworks=compliance_frameworks
        )

class RuleModel(BaseModel):
    """API model for audit rules."""
    id: str
    name: str
    description: str
    category: str
    severity: SeverityModel
    enabled: bool = True
    languages: List[str] = []
    tags: List[str] = []
    
    @classmethod
    def from_rule(cls, rule) -> 'RuleModel':
        """Convert core Rule to API model."""
        return cls(
            id=rule.id,
            name=getattr(rule, 'name', rule.id),
            description=rule.description,
            category=rule.category,
            severity=SeverityModel(rule.severity.value),
            enabled=True,
            languages=getattr(rule, 'languages', []),
            tags=getattr(rule, 'tags', [])
        )

class ConfigModel(BaseModel):
    """API model for auditor configuration."""
    min_severity: SeverityModel = SeverityModel.MEDIUM
    enabled_rules: List[str] = []
    disabled_rules: List[str] = []
    exclude_patterns: List[str] = []
    include_patterns: List[str] = []
    max_issues_per_file: int = 50
    include_code_snippets: bool = True
    show_remediation: bool = True
    check_data_privacy: bool = True
    check_model_security: bool = True
    check_bias_detection: bool = True
    
    @classmethod
    def from_config(cls, config: AuditorConfig) -> 'ConfigModel':
        """Convert core config to API model."""
        return cls(
            min_severity=SeverityModel(config.min_severity),
            enabled_rules=config.enabled_rules,
            disabled_rules=config.disabled_rules,
            exclude_patterns=config.exclude_patterns,
            include_patterns=config.include_patterns,
            max_issues_per_file=config.max_issues_per_file,
            include_code_snippets=config.include_code_snippets,
            show_remediation=config.show_remediation,
            check_data_privacy=config.check_data_privacy,
            check_model_security=config.check_model_security,
            check_bias_detection=config.check_bias_detection
        )

class ScanRequest(BaseModel):
    """Request model for starting a scan."""
    config: Optional[ConfigModel] = None
    webhook_url: Optional[str] = None

class ScanResponse(BaseModel):
    """Response model for scan initiation."""
    scan_id: str
    status: str
    message: str

class ScanStatusResponse(BaseModel):
    """Response model for scan status."""
    scan_id: str
    status: str
    progress: int = Field(ge=0, le=100)
    start_time: datetime
    end_time: Optional[datetime] = None
    message: str = ""

class ScanSummary(BaseModel):
    """Summary statistics for scan results."""
    total_issues: int
    critical: int
    high: int
    medium: int
    low: int
    files_scanned: int
    files_with_errors: int

class FrameworkModel(BaseModel):
    """API model for detected frameworks."""
    name: str
    type: str
    confidence: float
    files: List[str] = []

class ScanResultsResponse(BaseModel):
    """Response model for scan results."""
    scan_id: str
    summary: ScanSummary
    issues: List[IssueModel]
    errors: Dict[str, str] = {}
    detected_frameworks: Dict[str, FrameworkModel] = {}
    compliance_summary: Dict[str, Dict] = {}

class WebSocketMessage(BaseModel):
    """WebSocket message model."""
    type: str
    scan_id: str
    data: Dict[str, Any] = {}

class GitHubIntegrationRequest(BaseModel):
    """Request model for GitHub integration."""
    repository_url: str
    branch: str = "main"
    access_token: Optional[str] = None
    webhook_url: Optional[str] = None

class ReportRequest(BaseModel):
    """Request model for generating reports."""
    scan_id: str
    format: str = Field(pattern="^(html|pdf|json|csv)$")
    include_remediation: bool = True
    severity_filter: Optional[SeverityModel] = None