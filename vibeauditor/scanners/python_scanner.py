"""
Python file scanner.
"""

import ast
from pathlib import Path
from typing import Optional, Any

from .base_scanner import BaseScanner

class PythonScanner(BaseScanner):
    """Scanner for Python files."""
    
    def __init__(self):
        super().__init__()
        self.supported_extensions = ['.py']
    
    def parse_file(self, file_path: Path) -> Optional[Any]:
        """Parse Python file using AST."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse to AST
            tree = ast.parse(content, filename=str(file_path))
            return tree
            
        except (SyntaxError, UnicodeDecodeError, FileNotFoundError):
            # Return None if parsing fails
            return None