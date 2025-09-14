"""
Console reporter for audit results.
"""

from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

from ..core.results import AuditResults, Severity

class ConsoleReporter:
    """Console-based reporter for audit results."""
    
    def __init__(self, verbose: bool = False):
        self.console = Console()
        self.verbose = verbose
    
    def generate_report(self, results: AuditResults, output_path: Optional[Path] = None):
        """Generate console report."""
        
        # Framework detection results
        if hasattr(results, 'detected_frameworks') and results.detected_frameworks:
            self._print_frameworks(results.detected_frameworks)
        
        # Summary
        summary = results.get_summary()
        self._print_summary(summary)
        
        # Issues by severity
        if results.issues:
            self._print_issues(results)
        
        # Errors
        if results.errors:
            self._print_errors(results.errors)
        
        # Compliance Summary
        if hasattr(results, 'compliance_summary') and results.compliance_summary:
            self._print_compliance_summary(results.compliance_summary)
        
        # Recommendations
        self._print_recommendations(results)
    
    def _print_summary(self, summary: dict):
        """Print summary statistics."""
        table = Table(title="Audit Summary", show_header=True, header_style="bold magenta")
        table.add_column("Metric", style="cyan")
        table.add_column("Count", justify="right", style="green")
        
        table.add_row("Files Scanned", str(summary["files_scanned"]))
        table.add_row("Total Issues", str(summary["total_issues"]))
        table.add_row("Critical", str(summary["critical"]), style="red")
        table.add_row("High", str(summary["high"]), style="orange1")
        table.add_row("Medium", str(summary["medium"]), style="yellow")
        table.add_row("Low", str(summary["low"]), style="green")
        
        if summary["files_with_errors"] > 0:
            table.add_row("Files with Errors", str(summary["files_with_errors"]), style="red")
        
        self.console.print(table)
        self.console.print()
    
    def _print_issues(self, results: AuditResults):
        """Print issues grouped by severity."""
        
        for severity in [Severity.CRITICAL, Severity.HIGH, Severity.MEDIUM, Severity.LOW]:
            issues = results.get_issues_by_severity(severity)
            if not issues:
                continue
            
            # Color mapping
            colors = {
                Severity.CRITICAL: "red",
                Severity.HIGH: "orange1", 
                Severity.MEDIUM: "yellow",
                Severity.LOW: "green"
            }
            
            color = colors[severity]
            
            self.console.print(f"\n[bold {color}]{severity.value.upper()} SEVERITY ISSUES ({len(issues)})[/bold {color}]")
            
            for issue in issues:
                self._print_issue(issue, color)
    
    def _print_issue(self, issue, color: str):
        """Print a single issue."""
        
        # Issue header
        location = f"{issue.file_path}"
        if issue.line_number:
            location += f":{issue.line_number}"
        if issue.column_number:
            location += f":{issue.column_number}"
        
        header = f"[{color}]●[/{color}] {issue.rule_id} - {location}"
        self.console.print(header)
        
        # Message
        self.console.print(f"  {issue.message}")
        
        # Code snippet
        if issue.code_snippet and self.verbose:
            self.console.print(f"  [dim]Code:[/dim] {issue.code_snippet}")
        
        # Remediation
        if issue.remediation and self.verbose:
            self.console.print(f"  [dim]Fix:[/dim] {issue.remediation}")
        
        # Standards and Compliance
        if hasattr(issue, 'standards') and issue.standards and self.verbose:
            standards_text = ", ".join([f"{std.name}" for std in issue.standards[:3]])
            if len(issue.standards) > 3:
                standards_text += f" (+{len(issue.standards) - 3} more)"
            self.console.print(f"  [dim]Standards:[/dim] {standards_text}")
        
        if hasattr(issue, 'compliance_frameworks') and issue.compliance_frameworks and self.verbose:
            compliance_text = ", ".join(issue.compliance_frameworks[:2])
            if len(issue.compliance_frameworks) > 2:
                compliance_text += f" (+{len(issue.compliance_frameworks) - 2} more)"
            self.console.print(f"  [dim]Compliance:[/dim] {compliance_text}")
        
        self.console.print()
    
    def _print_errors(self, errors: dict):
        """Print processing errors."""
        if not errors:
            return
        
        self.console.print("\n[bold red]PROCESSING ERRORS[/bold red]")
        
        for file_path, error_msg in errors.items():
            self.console.print(f"[red]●[/red] {file_path}: {error_msg}")
        
        self.console.print()
    
    def _print_recommendations(self, results: AuditResults):
        """Print general recommendations."""
        summary = results.get_summary()
        
        recommendations = []
        
        if summary["critical"] > 0:
            recommendations.append("🚨 Address critical security issues immediately")
        
        if summary["high"] > 0:
            recommendations.append("⚠️  Review and fix high-severity issues")
        
        if summary["total_issues"] > 50:
            recommendations.append("📊 Consider implementing automated code quality checks")
        
        if summary["files_with_errors"] > 0:
            recommendations.append("🔧 Fix file processing errors to get complete analysis")
        
        if recommendations:
            panel = Panel(
                "\n".join(recommendations),
                title="[bold blue]Recommendations[/bold blue]",
                border_style="blue"
            )
            self.console.print(panel)
    
    def _print_frameworks(self, frameworks: dict):
        """Print detected frameworks."""
        if not frameworks:
            return
        
        table = Table(title="Detected Frameworks", show_header=True, header_style="bold blue")
        table.add_column("Framework", style="cyan")
        table.add_column("Type", style="magenta")
        table.add_column("Confidence", justify="right", style="green")
        table.add_column("Files", style="yellow")
        
        for name, framework in frameworks.items():
            confidence_str = f"{framework.confidence:.1%}"
            files_str = f"{len(framework.files)} files" if framework.files else "N/A"
            
            table.add_row(
                framework.name,
                framework.type.value if hasattr(framework.type, 'value') else str(framework.type),
                confidence_str,
                files_str
            )
        
        self.console.print(table)
        self.console.print()    
    d
ef _print_compliance_summary(self, compliance_summary: dict):
        """Print compliance framework summary."""
        if not compliance_summary:
            return
        
        table = Table(title="Compliance Framework Impact", show_header=True, header_style="bold red")
        table.add_column("Framework", style="cyan")
        table.add_column("Issues", justify="right", style="yellow")
        table.add_column("Critical", justify="right", style="red")
        table.add_column("High", justify="right", style="orange1")
        table.add_column("Medium", justify="right", style="yellow")
        table.add_column("Low", justify="right", style="green")
        
        for framework_id, data in compliance_summary.items():
            table.add_row(
                data["name"][:50] + "..." if len(data["name"]) > 50 else data["name"],
                str(data["count"]),
                str(data["critical"]),
                str(data["high"]),
                str(data["medium"]),
                str(data["low"])
            )
        
        self.console.print(table)
        self.console.print()