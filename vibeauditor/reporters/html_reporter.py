"""
HTML reporter for audit results.
"""

from pathlib import Path
from typing import Optional
from jinja2 import Template

from ..core.results import AuditResults, Severity

class HTMLReporter:
    """HTML-based reporter for audit results."""
    
    def __init__(self):
        self.template = self._get_template()
    
    def generate_report(self, results: AuditResults, output_path: Optional[Path] = None):
        """Generate HTML report."""
        
        summary = results.get_summary()
        
        # Group issues by file and severity
        issues_by_file = {}
        for issue in results.issues:
            file_key = str(issue.file_path)
            if file_key not in issues_by_file:
                issues_by_file[file_key] = []
            issues_by_file[file_key].append(issue)
        
        # Sort issues by severity
        for file_issues in issues_by_file.values():
            file_issues.sort(key=lambda x: x.severity.value, reverse=True)
        
        html_content = self.template.render(
            summary=summary,
            issues_by_file=issues_by_file,
            errors=results.errors,
            severity_colors=self._get_severity_colors()
        )
        
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
        else:
            print(html_content)
    
    def _get_severity_colors(self):
        """Get color mapping for severities."""
        return {
            Severity.CRITICAL: "#dc2626",
            Severity.HIGH: "#ea580c", 
            Severity.MEDIUM: "#d97706",
            Severity.LOW: "#16a34a"
        }
    
    def _get_template(self):
        """Get HTML template."""
        template_str = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VibeCodeAuditor Report</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 20px; background: #f8fafc; }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { background: white; padding: 30px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); margin-bottom: 20px; }
        .summary { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 20px; margin: 20px 0; }
        .summary-card { background: white; padding: 20px; border-radius: 8px; text-align: center; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
        .summary-card h3 { margin: 0 0 10px 0; font-size: 2em; }
        .summary-card p { margin: 0; color: #6b7280; }
        .critical { color: #dc2626; }
        .high { color: #ea580c; }
        .medium { color: #d97706; }
        .low { color: #16a34a; }
        .file-section { background: white; margin: 20px 0; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
        .file-header { padding: 20px; border-bottom: 1px solid #e5e7eb; font-weight: bold; }
        .issue { padding: 20px; border-bottom: 1px solid #f3f4f6; }
        .issue:last-child { border-bottom: none; }
        .issue-header { display: flex; align-items: center; margin-bottom: 10px; }
        .severity-badge { padding: 4px 8px; border-radius: 4px; color: white; font-size: 0.8em; margin-right: 10px; }
        .code-snippet { background: #f8fafc; padding: 10px; border-radius: 4px; font-family: monospace; margin: 10px 0; }
        .remediation { background: #f0f9ff; padding: 10px; border-radius: 4px; border-left: 4px solid #0ea5e9; margin: 10px 0; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>VibeCodeAuditor Report</h1>
            <p>Comprehensive code audit results</p>
        </div>
        
        <div class="summary">
            <div class="summary-card">
                <h3>{{ summary.files_scanned }}</h3>
                <p>Files Scanned</p>
            </div>
            <div class="summary-card">
                <h3>{{ summary.total_issues }}</h3>
                <p>Total Issues</p>
            </div>
            <div class="summary-card">
                <h3 class="critical">{{ summary.critical }}</h3>
                <p>Critical</p>
            </div>
            <div class="summary-card">
                <h3 class="high">{{ summary.high }}</h3>
                <p>High</p>
            </div>
            <div class="summary-card">
                <h3 class="medium">{{ summary.medium }}</h3>
                <p>Medium</p>
            </div>
            <div class="summary-card">
                <h3 class="low">{{ summary.low }}</h3>
                <p>Low</p>
            </div>
        </div>
        
        {% for file_path, issues in issues_by_file.items() %}
        <div class="file-section">
            <div class="file-header">{{ file_path }}</div>
            {% for issue in issues %}
            <div class="issue">
                <div class="issue-header">
                    <span class="severity-badge" style="background-color: {{ severity_colors[issue.severity] }}">
                        {{ issue.severity.value.upper() }}
                    </span>
                    <strong>{{ issue.rule_id }}</strong>
                    {% if issue.line_number %}
                    <span style="color: #6b7280; margin-left: 10px;">Line {{ issue.line_number }}</span>
                    {% endif %}
                </div>
                <p>{{ issue.message }}</p>
                {% if issue.code_snippet %}
                <div class="code-snippet">{{ issue.code_snippet }}</div>
                {% endif %}
                {% if issue.remediation %}
                <div class="remediation">
                    <strong>Remediation:</strong> {{ issue.remediation }}
                </div>
                {% endif %}
            </div>
            {% endfor %}
        </div>
        {% endfor %}
        
        {% if errors %}
        <div class="file-section">
            <div class="file-header" style="color: #dc2626;">Processing Errors</div>
            {% for file_path, error in errors.items() %}
            <div class="issue">
                <strong>{{ file_path }}</strong>
                <p>{{ error }}</p>
            </div>
            {% endfor %}
        </div>
        {% endif %}
    </div>
</body>
</html>
        """
        return Template(template_str)