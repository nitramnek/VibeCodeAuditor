import pytest
import ast
from pathlib import Path
from vibeauditor.rules.ai_ml_rules import (
    ASTDataPrivacyRule, ModelExplainabilityRule, 
    PrivacyAnalyzer, ExplainabilityAnalyzer
)

@pytest.fixture
def sample_code_dir(tmp_path):
    code_dir = tmp_path / "code"
    code_dir.mkdir()
    return code_dir

def test_ast_privacy_rule_detects_sensitive_vars(sample_code_dir):
    test_file = sample_code_dir / "test.py"
    test_file.write_text("user_email = 'test@example.com'")
    
    rule = ASTDataPrivacyRule()
    issues = rule.check(test_file)
    
    assert len(issues) == 1
    assert "Sensitive term 'user_email'" in issues[0].message

def test_explainability_rule_detects_missing_imports(sample_code_dir):
    test_file = sample_code_dir / "model.py"
    test_file.write_text("import pandas as pd\nmodel = LinearRegression()")
    
    rule = ModelExplainabilityRule()
    issues = rule.check(test_file)
    
    assert len(issues) == 1
    assert "lacks explainability features" in issues[0].message

def test_privacy_analyzer_checks_anonymization():
    code = """
def process_data():
    anonymize(user_data, salt='secure_salt')
"""
    tree = ast.parse(code)
    analyzer = PrivacyAnalyzer({'user_data'})
    analyzer.visit(tree)
    assert len(analyzer.issues) == 0

def test_explainability_analyzer_detects_shap():
    code = "import shap\nshap.Explainer(model)"
    tree = ast.parse(code)
    analyzer = ExplainabilityAnalyzer({'shap'})
    analyzer.visit(tree)
    assert analyzer.found_explanations is True