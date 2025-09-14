"""
Rule management for VibeCodeAuditor.
"""

from .base_rule import BaseRule
from .security_rules import SecurityRules
from .quality_rules import QualityRules
from .ai_ml_rules import AIMLRules
from .framework_rules import FrameworkRules

def get_all_rules():
    """Get all available audit rules."""
    rules = []
    
    # Add security rules
    rules.extend(SecurityRules.get_rules())
    
    # Add quality rules
    rules.extend(QualityRules.get_rules())
    
    # Add AI/ML specific rules
    rules.extend(AIMLRules.get_rules())
    
    # Add framework-specific rules
    rules.extend(FrameworkRules.get_rules())
    
    return rules

def get_enabled_rules(config):
    """Get enabled rules based on configuration."""
    all_rules = get_all_rules()
    
    if not config.enabled_rules:
        # If no specific rules enabled, use all except disabled
        return [rule for rule in all_rules if config.is_rule_enabled(rule.id)]
    else:
        # Only use specifically enabled rules
        return [rule for rule in all_rules if rule.id in config.enabled_rules]

__all__ = ["BaseRule", "get_all_rules", "get_enabled_rules"]