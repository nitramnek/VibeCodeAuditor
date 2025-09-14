"""
Configuration management for VibeCodeAuditor.
"""

import yaml
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field

@dataclass
class AuditorConfig:
    """Configuration for the code auditor."""
    
    # Scanning options
    min_severity: str = "medium"
    enabled_rules: List[str] = field(default_factory=list)
    disabled_rules: List[str] = field(default_factory=list)
    exclude_patterns: List[str] = field(default_factory=lambda: [
        "*.pyc", "__pycache__", ".git", "node_modules", ".venv", "venv"
    ])
    include_patterns: List[str] = field(default_factory=lambda: [
        "*.py", "*.js", "*.ts", "*.java", "*.go", "*.rs", "*.cpp", "*.c"
    ])
    
    # Language-specific settings
    python_settings: Dict[str, Any] = field(default_factory=dict)
    javascript_settings: Dict[str, Any] = field(default_factory=dict)
    java_settings: Dict[str, Any] = field(default_factory=dict)
    
    # AI/ML specific settings
    check_data_privacy: bool = True
    check_model_security: bool = True
    check_bias_detection: bool = True
    
    # Report settings
    max_issues_per_file: int = 50
    include_code_snippets: bool = True
    show_remediation: bool = True
    
    @classmethod
    def from_file(cls, config_path: Path) -> 'AuditorConfig':
        """Load configuration from YAML file."""
        with open(config_path, 'r') as f:
            data = yaml.safe_load(f)
        
        return cls(**data)
    
    def to_file(self, config_path: Path) -> None:
        """Save configuration to YAML file."""
        with open(config_path, 'w') as f:
            yaml.dump(self.__dict__, f, default_flow_style=False)
    
    def is_rule_enabled(self, rule_id: str) -> bool:
        """Check if a specific rule is enabled."""
        if self.disabled_rules and rule_id in self.disabled_rules:
            return False
        if self.enabled_rules:
            return rule_id in self.enabled_rules
        return True
    
    def should_scan_file(self, file_path: Path) -> bool:
        """Check if a file should be scanned based on patterns."""
        file_str = str(file_path)
        
        # Check exclude patterns
        for pattern in self.exclude_patterns:
            if file_path.match(pattern):
                return False
        
        # Check include patterns
        if self.include_patterns:
            for pattern in self.include_patterns:
                if file_path.match(pattern):
                    return True
            return False
        
        return True