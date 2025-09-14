"""Tests for the main auditor functionality."""

import pytest
from pathlib import Path
from vibeauditor.core.auditor import CodeAuditor
from vibeauditor.core.config import AuditorConfig

def test_auditor_initialization():
    """Test auditor initialization with default config."""
    config = AuditorConfig()
    auditor = CodeAuditor(config)
    assert auditor.config == config
    assert len(auditor.rules) > 0

def test_scan_single_file():
    """Test scanning a single file."""
    config = AuditorConfig()
    auditor = CodeAuditor(config)
    
    # Create a test file
    test_file = Path("test_file.py")
    test_content = '''
import os
API_KEY = "secret123"
def test_function():
    pass
'''
    
    try:
        with open(test_file, 'w') as f:
            f.write(test_content)
        
        results = auditor.scan(test_file)
        assert results is not None
        assert len(results.issues) > 0  # Should find hardcoded secret
        
    finally:
        if test_file.exists():
            test_file.unlink()

def test_config_rule_filtering():
    """Test that config properly filters rules."""
    config = AuditorConfig()
    config.disabled_rules = ["hardcodedsecretsrule"]
    
    auditor = CodeAuditor(config)
    rule_ids = [rule.id for rule in auditor.rules]
    assert "hardcodedsecretsrule" not in rule_ids