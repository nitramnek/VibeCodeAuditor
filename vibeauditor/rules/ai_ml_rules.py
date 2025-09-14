"""
AI/ML specific audit rules.
"""

import re
import ast
from pathlib import Path
from typing import List, Optional, Any, Dict
from .base_rule import BaseRule
from ..core.results import Issue, Severity

class ASTDataPrivacyRule(BaseRule):
    """Detect potential data privacy issues using AST analysis."""
    
    def __init__(self):
        super().__init__(
            rule_id="ai_ml.ast_data_privacy",
            description="Detects data privacy issues using abstract syntax tree analysis",
            severity=Severity.HIGH,
            category="ai_ml"
        )
        self.languages = ['.py']
        self.sensitive_terms = {
            'email', 'ssn', 'credit_card', 'passport',
            'gdpr', 'ccpa', 'hipaa', 'pii'
        }
    
    def check(self, file_path: Path, parsed_content: Optional[Any] = None) -> List[Issue]:
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read())

            analyzer = PrivacyAnalyzer(self.sensitive_terms)
            analyzer.visit(tree)

            for node in analyzer.issues:
                issues.append(self.create_issue(
                    file_path=file_path,
                    message=f"Potential privacy concern: {node['reason']}",
                    line_number=node['lineno'],
                    code_snippet=node['snippet'],
                    remediation="Implement data anonymization or pseudonymization",
                    confidence=0.8
                ))

        except Exception as e:
            pass

        return issues

class PrivacyAnalyzer(ast.NodeVisitor):
    def __init__(self, sensitive_terms: set):
        self.sensitive_terms = sensitive_terms
        self.issues = []

    def visit_Name(self, node):
        if node.id.lower() in self.sensitive_terms:
            self._add_issue(node, f"Sensitive term '{node.id}' detected in variable name")

    def visit_Call(self, node):
        if isinstance(node.func, ast.Attribute):
            func_name = node.func.attr.lower()
            if func_name in {'anonymize', 'pseudonymize'}:
                self._check_anonymization(node)

    def _check_anonymization(self, node):
        if not any(kw.arg == 'salt' for kw in node.keywords):
            self._add_issue(node, "Anonymization without cryptographic salt")

    def _add_issue(self, node, reason: str):
        self.issues.append({
            'lineno': node.lineno,
            'snippet': ast.get_source_segment(node),
            'reason': reason
        })

class DataPrivacyRule(BaseRule):
    """Detect potential data privacy issues using regex patterns."""
    
    def __init__(self):
        super().__init__(
            rule_id="ai_ml.data_privacy",
            description="Detects data privacy issues using regex patterns",
            severity=Severity.HIGH,
            category="ai_ml"
        )
        self.languages = ['.py']
    
    def check(self, file_path: Path, parsed_content: Optional[Any] = None) -> List[Issue]:
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            
            # Patterns that might indicate privacy concerns
            privacy_patterns = [
                (r'(?i)(email|phone|ssn|social.security|credit.card|passport)', "Potential PII data handling"),
                (r'(?i)(gdpr|ccpa|hipaa)', "Privacy regulation mentioned - ensure compliance"),
                (r'(?i)(personal.data|sensitive.data|private.data)', "Sensitive data handling detected"),
                (r'(?i)(anonymize|pseudonymize|de.identify)', "Data anonymization - verify implementation"),
            ]
            
            for line_num, line in enumerate(lines, 1):
                for pattern, message in privacy_patterns:
                    if re.search(pattern, line):
                        issues.append(self.create_issue(
                            file_path=file_path,
                            message=message,
                            line_number=line_num,
                            code_snippet=line.strip(),
                            remediation="Ensure proper data privacy measures and compliance with regulations",
                            confidence=0.6,
                            metadata={"privacy_concern": True}
                        ))
        
        except Exception:
            pass
        
        return issues

class ModelSecurityRule(BaseRule):
    """Detect potential model security issues."""
    
    def __init__(self):
        super().__init__(
            rule_id="ai_ml.model_security",
            description="Detects potential security issues in ML model handling",
            severity=Severity.MEDIUM,
            category="ai_ml"
        )
        self.languages = ['.py']
    
    def check(self, file_path: Path, parsed_content: Optional[Any] = None) -> List[Issue]:
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            
            # Model security patterns
            security_patterns = [
                (r'pickle\.load\(', "Pickle deserialization can be unsafe - consider alternatives"),
                (r'joblib\.load\(', "Joblib loading can be unsafe with untrusted data"),
                (r'torch\.load\(.*map_location=None', "PyTorch model loading without map_location can be unsafe"),
                (r'tf\.saved_model\.load\(', "TensorFlow model loading - ensure model source is trusted"),
                (r'(?i)model.*download.*http', "Model downloaded from HTTP - use HTTPS for security"),
            ]
            
            for line_num, line in enumerate(lines, 1):
                for pattern, message in security_patterns:
                    if re.search(pattern, line):
                        issues.append(self.create_issue(
                            file_path=file_path,
                            message=message,
                            line_number=line_num,
                            code_snippet=line.strip(),
                            remediation="Use secure model loading practices and verify model integrity",
                            confidence=0.7,
                            metadata={"security_concern": "model_loading"}
                        ))
        
        except Exception:
            pass
        
        return issues

class BiasDetectionRule(BaseRule):
    """Detect potential bias issues in AI/ML code."""
    
    def __init__(self):
        super().__init__(
            rule_id="ai_ml.bias_detection",
            description="Detects potential bias issues in AI/ML workflows",
            severity=Severity.MEDIUM,
            category="ai_ml"
        )
        self.languages = ['.py']
    
    def check(self, file_path: Path, parsed_content: Optional[Any] = None) -> List[Issue]:
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            
            # Bias-related patterns
            bias_patterns = [
                (r'(?i)(gender|race|ethnicity|age|religion)', "Demographic features detected - check for bias"),
                (r'(?i)(fairness|bias|discrimination)', "Bias-related terms found - ensure proper handling"),
                (r'(?i)(protected.attribute|sensitive.attribute)', "Protected attributes detected"),
                (r'train_test_split\(.*stratify=None', "Data splitting without stratification may introduce bias"),
            ]
            
            for line_num, line in enumerate(lines, 1):
                for pattern, message in bias_patterns:
                    if re.search(pattern, line):
                        issues.append(self.create_issue(
                            file_path=file_path,
                            message=message,
                            line_number=line_num,
                            code_snippet=line.strip(),
                            remediation="Implement bias detection and mitigation strategies",
                            confidence=0.5,
                            metadata={"bias_concern": True}
                        ))
        
        except Exception:
            pass
        
        return issues

class DataValidationRule(BaseRule):
    """Detect missing data validation in AI/ML pipelines."""
    
    def __init__(self):
        super().__init__(
            rule_id="ai_ml.data_validation",
            description="Detects missing data validation in AI/ML workflows",
            severity=Severity.MEDIUM,
            category="ai_ml"
        )
        self.languages = ['.py']
    
    def check(self, file_path: Path, parsed_content: Optional[Any] = None) -> List[Issue]:
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.splitlines()
            
            # Check for data loading without validation
            has_data_loading = bool(re.search(r'(?i)(pd\.read_|np\.load|torch\.load|tf\.data)', content))
            has_validation = bool(re.search(r'(?i)(assert|validate|check|verify|isna|isnull)', content))
            
            if has_data_loading and not has_validation:
                # Find the data loading line
                for line_num, line in enumerate(lines, 1):
                    if re.search(r'(?i)(pd\.read_|np\.load|torch\.load|tf\.data)', line):
                        issues.append(self.create_issue(
                            file_path=file_path,
                            message="Data loading detected without apparent validation",
                            line_number=line_num,
                            code_snippet=line.strip(),
                            remediation="Add data validation checks (null values, data types, ranges, etc.)",
                            confidence=0.6,
                            metadata={"validation_missing": True}
                        ))
                        break
        
        except Exception:
            pass
        
        return issues

class ModelExplainabilityRule(BaseRule):
    """Detect missing model explainability features."""
    
    def __init__(self):
        super().__init__(
            rule_id="ai_ml.explainability",
            description="Checks for model explainability implementations",
            severity=Severity.MEDIUM,
            category="ai_ml"
        )
        self.languages = ['.py']
        self.required_explanations = {
            'shap', 'lime', 'eli5', 'interpret',
            'shap.Explainer', 'shap.TreeExplainer'
        }

    def check(self, file_path: Path, parsed_content: Optional[Any] = None) -> List[Issue]:
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read())

            analyzer = ExplainabilityAnalyzer(self.required_explanations)
            analyzer.visit(tree)

            if not analyzer.found_explanations:
                issues.append(self.create_issue(
                    file_path=file_path,
                    message="Model implementation lacks explainability features",
                    line_number=1,  # File-level issue
                    code_snippet="",
                    remediation="Implement SHAP, LIME, or other explainability frameworks",
                    confidence=0.7
                ))

        except Exception as e:
            pass

        return issues

class ExplainabilityAnalyzer(ast.NodeVisitor):
    def __init__(self, required_explanations: set):
        self.required_explanations = required_explanations
        self.found_explanations = False

    def visit_Import(self, node):
        for alias in node.names:
            if alias.name.split('.')[0] in self.required_explanations:
                self.found_explanations = True

    def visit_ImportFrom(self, node):
        if node.module and any(part in self.required_explanations for part in node.module.split('.')):
            self.found_explanations = True

    def visit_Call(self, node):
        if isinstance(node.func, ast.Attribute):
            func_name = node.func.attr
            if func_name in {'explain', 'summary_plot', 'force_plot'}:
                self.found_explanations = True

class AIMLRules:
    """Collection of AI/ML specific rules."""
    
    @staticmethod
    def get_rules() -> List[BaseRule]:
        """Get all AI/ML rules."""
        return [
            DataPrivacyRule(),  # Keep legacy regex-based rule for non-Python files
            ASTDataPrivacyRule(),
            ModelSecurityRule(),
            BiasDetectionRule(),
            DataValidationRule(),
            ModelExplainabilityRule(),
        ]
