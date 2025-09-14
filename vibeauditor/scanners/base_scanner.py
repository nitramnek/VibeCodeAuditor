"""
Base scanner class for different file types.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, Any

class BaseScanner(ABC):
    """Base class for file scanners."""
    
    def __init__(self):
        self.supported_extensions = []
    
    @abstractmethod
    def parse_file(self, file_path: Path) -> Optional[Any]:
        """Parse file and return structured representation."""
        pass
    
    def supports_file(self, file_path: Path) -> bool:
        """Check if scanner supports the given file type."""
        return file_path.suffix.lower() in self.supported_extensions