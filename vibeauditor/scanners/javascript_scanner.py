"""
JavaScript/TypeScript file scanner.
"""

from pathlib import Path
from typing import Optional, Any

from .base_scanner import BaseScanner

class JavaScriptScanner(BaseScanner):
    """Scanner for JavaScript/TypeScript files."""
    
    def __init__(self):
        super().__init__()
        self.supported_extensions = ['.js', '.ts', '.jsx', '.tsx']
    
    def parse_file(self, file_path: Path) -> Optional[Any]:
        """Parse JavaScript/TypeScript file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # For now, return raw content
            # In a full implementation, you'd use a JS parser like esprima
            return {
                'content': content,
                'lines': content.splitlines(),
                'type': 'javascript'
            }
            
        except (UnicodeDecodeError, FileNotFoundError):
            return None