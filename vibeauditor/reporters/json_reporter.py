"""
JSON reporter for audit results.
"""

import json
from pathlib import Path
from typing import Optional

from ..core.results import AuditResults

class JSONReporter:
    """JSON-based reporter for audit results."""
    
    def __init__(self):
        pass
    
    def generate_report(self, results: AuditResults, output_path: Optional[Path] = None):
        """Generate JSON report."""
        
        report_data = results.to_dict()
        
        # Add metadata
        report_data["metadata"] = {
            "format": "json",
            "version": "1.0",
            "generator": "VibeCodeAuditor"
        }
        
        json_output = json.dumps(report_data, indent=2, default=str)
        
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(json_output)
        else:
            print(json_output)