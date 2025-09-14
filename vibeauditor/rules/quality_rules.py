"""
Code quality audit rules.
"""

import re
from pathlib import Path
from typing import List, Optional, Any

from .base_rule import BaseRule
from ..core.results import Issue, Severity

class LongFunctionRule(BaseRule):
    """Detect overly long functions."""
    
    def __init__(self, max_lines: int = 50):
        super().__init__(
            rule_id="quality.long_function",
            description=f"Detects functions longer than {max_lines} lines",
            severity=Severity.MEDIUM,
            category="quality"
        )
        self.max_lines = max_lines
        self.languages = ['.py', '.js', '.ts', '.java']
    
    def check(self, file_path: Path, parsed_content: Optional[Any] = None) -> List[Issue]:
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            
            # Simple function detection (can be improved with AST parsing)
            function_patterns = [
                r'^\s*def\s+(\w+)\s*\(',  # Python
                r'^\s*function\s+(\w+)\s*\(',  # JavaScript
                r'^\s*(\w+)\s*\([^)]*\)\s*{',  # JavaScript/TypeScript arrow functions
            ]
            
            current_function = None
            function_start = 0
            indent_level = 0
            
            for line_num, line in enumerate(lines, 1):
                # Check for function start
                for pattern in function_patterns:
                    match = re.search(pattern, line)
                    if match:
                        if current_function:
                            # End previous function
                            self._check_function_length(
                                issues, file_path, current_function, 
                                function_start, line_num - 1, lines
                            )
                        
                        current_function = match.group(1)
                        function_start = line_num
                        indent_level = len(line) - len(line.lstrip())
                        break
                
                # Check for function end (simplified)
                if current_function and line.strip():
                    current_indent = len(line) - len(line.lstrip())
                    if current_indent <= indent_level and line_num > function_start + 1:
                        self._check_function_length(
                            issues, file_path, current_function,
                            function_start, line_num - 1, lines
                        )
                        current_function = None
            
            # Check last function if file ends
            if current_function:
                self._check_function_length(
                    issues, file_path, current_function,
                    function_start, len(lines), lines
                )
        
        except Exception:
            pass
        
        return issues
    
    def _check_function_length(self, issues, file_path, func_name, start_line, end_line, lines):
        """Check if function exceeds maximum length."""
        func_length = end_line - start_line + 1
        if func_length > self.max_lines:
            issues.append(self.create_issue(
                file_path=file_path,
                message=f"Function '{func_name}' is {func_length} lines long (max: {self.max_lines})",
                line_number=start_line,
                code_snippet=lines[start_line - 1].strip() if start_line <= len(lines) else "",
                remediation="Consider breaking this function into smaller, more focused functions",
                confidence=0.9,
                metadata={"function_name": func_name, "length": func_length}
            ))

class TodoCommentRule(BaseRule):
    """Detect TODO comments that might indicate incomplete work."""
    
    def __init__(self):
        super().__init__(
            rule_id="quality.todo_comments",
            description="Detects TODO, FIXME, and HACK comments",
            severity=Severity.LOW,
            category="quality"
        )
    
    def check(self, file_path: Path, parsed_content: Optional[Any] = None) -> List[Issue]:
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            
            todo_patterns = [
                (r'(?i)#.*\b(TODO|FIXME|HACK|BUG)\b', "TODO/FIXME comment found"),
                (r'(?i)//.*\b(TODO|FIXME|HACK|BUG)\b', "TODO/FIXME comment found"),
                (r'(?i)/\*.*\b(TODO|FIXME|HACK|BUG)\b.*\*/', "TODO/FIXME comment found"),
            ]
            
            for line_num, line in enumerate(lines, 1):
                for pattern, message in todo_patterns:
                    if re.search(pattern, line):
                        issues.append(self.create_issue(
                            file_path=file_path,
                            message=message,
                            line_number=line_num,
                            code_snippet=line.strip(),
                            remediation="Address the TODO/FIXME or create a proper issue tracker item",
                            confidence=1.0
                        ))
        
        except Exception:
            pass
        
        return issues

class DeadCodeRule(BaseRule):
    """Detect potentially dead/unreachable code."""
    
    def __init__(self):
        super().__init__(
            rule_id="quality.dead_code",
            description="Detects potentially unreachable or dead code",
            severity=Severity.LOW,
            category="quality"
        )
        self.languages = ['.py', '.js', '.ts']
    
    def check(self, file_path: Path, parsed_content: Optional[Any] = None) -> List[Issue]:
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            
            # Simple dead code patterns
            dead_code_patterns = [
                (r'^\s*return\s+.*\n.*\S', "Code after return statement"),
                (r'^\s*if\s+False\s*:', "Code in 'if False' block"),
                (r'^\s*if\s+0\s*:', "Code in 'if 0' block"),
            ]
            
            for line_num, line in enumerate(lines, 1):
                for pattern, message in dead_code_patterns:
                    if re.search(pattern, line):
                        # Check if there's code after return
                        if "return" in pattern and line_num < len(lines):
                            next_line = lines[line_num].strip()
                            if next_line and not next_line.startswith(('#', '//')):
                                issues.append(self.create_issue(
                                    file_path=file_path,
                                    message=message,
                                    line_number=line_num + 1,
                                    code_snippet=next_line,
                                    remediation="Remove unreachable code or restructure logic",
                                    confidence=0.8
                                ))
        
        except Exception:
            pass
        
        return issues

class QualityRules:
    """Collection of code quality rules."""
    
    @staticmethod
    def get_rules() -> List[BaseRule]:
        """Get all quality rules."""
        return [
            LongFunctionRule(),
            TodoCommentRule(),
            DeadCodeRule(),
        ]