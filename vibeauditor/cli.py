"""
Command-line interface for VibeCodeAuditor.
"""

import click
import sys
from pathlib import Path
from rich.console import Console
from rich.table import Table

from .core.auditor import CodeAuditor
from .core.config import AuditorConfig
from .reporters.console_reporter import ConsoleReporter
from .reporters.html_reporter import HTMLReporter
from .reporters.json_reporter import JSONReporter

console = Console()

@click.group()
@click.version_option()
def cli():
    """VibeCodeAuditor - Comprehensive code auditing for AI developers."""
    pass

@cli.command()
@click.argument('target_path', type=click.Path(exists=True))
@click.option('--config', '-c', type=click.Path(exists=True), help='Configuration file path')
@click.option('--report-format', '-f', type=click.Choice(['console', 'json', 'html']), 
              default='console', help='Report output format')
@click.option('--output', '-o', type=click.Path(), help='Output file path')
@click.option('--severity', '-s', type=click.Choice(['low', 'medium', 'high', 'critical']), 
              default='medium', help='Minimum severity level to report')
@click.option('--rules', '-r', multiple=True, help='Specific rules to run')
@click.option('--exclude', '-e', multiple=True, help='Patterns to exclude from scanning')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def scan(target_path, config, report_format, output, severity, rules, exclude, verbose):
    """Scan a codebase for security vulnerabilities and quality issues."""
    
    try:
        # Load configuration
        if config:
            auditor_config = AuditorConfig.from_file(config)
        else:
            auditor_config = AuditorConfig()
        
        # Override config with CLI options
        if severity:
            auditor_config.min_severity = severity
        if rules:
            auditor_config.enabled_rules = list(rules)
        if exclude:
            auditor_config.exclude_patterns.extend(exclude)
        
        # Initialize auditor
        auditor = CodeAuditor(auditor_config)
        
        # Run scan
        console.print(f"[bold blue]Scanning {target_path}...[/bold blue]")
        results = auditor.scan(Path(target_path))
        
        # Generate report
        if report_format == 'console':
            reporter = ConsoleReporter(verbose=verbose)
            reporter.generate_report(results, output)
        elif report_format == 'json':
            reporter = JSONReporter()
            reporter.generate_report(results, output)
        elif report_format == 'html':
            reporter = HTMLReporter()
            reporter.generate_report(results, output)
        
        # Exit with appropriate code
        if results.has_critical_issues():
            sys.exit(1)
        elif results.has_high_issues():
            sys.exit(2)
        else:
            sys.exit(0)
            
    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
        sys.exit(1)

@cli.command()
def list_rules():
    """List all available audit rules."""
    from .rules import get_all_rules
    
    table = Table(title="Available Audit Rules")
    table.add_column("Rule ID", style="cyan")
    table.add_column("Category", style="magenta")
    table.add_column("Severity", style="yellow")
    table.add_column("Description")
    
    for rule in get_all_rules():
        table.add_row(rule.id, rule.category, rule.severity, rule.description)
    
    console.print(table)

@cli.command()
@click.option('--host', default='127.0.0.1', help='Host to bind the server to')
@click.option('--port', default=8000, help='Port to bind the server to')
@click.option('--reload', is_flag=True, help='Enable auto-reload for development')
def serve(host, port, reload):
    """Start the VibeAuditor web server (PWA mode)."""
    try:
        import uvicorn
        from .api.main import app
        
        console.print(f"[bold green]Starting VibeAuditor web server...[/bold green]")
        console.print(f"[blue]Server will be available at: http://{host}:{port}[/blue]")
        console.print(f"[blue]API documentation: http://{host}:{port}/api/docs[/blue]")
        
        uvicorn.run(
            "vibeauditor.api.main:app",
            host=host,
            port=port,
            reload=reload,
            log_level="info"
        )
        
    except ImportError:
        console.print("[bold red]Error: FastAPI and uvicorn are required for web mode[/bold red]")
        console.print("Install with: pip install fastapi uvicorn[standard]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]Failed to start server: {e}[/bold red]")
        sys.exit(1)

def main():
    """Main entry point."""
    cli()

if __name__ == '__main__':
    main()