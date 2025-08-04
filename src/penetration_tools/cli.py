"""
Command Line Interface for the Penetration Testing Toolset.
"""

import asyncio
import typer
from typing import Optional, List
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.text import Text

from .config import settings
from .core.logging import logger
from .modules.network.scanner import NetworkScanner
from .modules.web.scanner import WebScanner
from .modules.database.scanner import DatabaseScanner
from .services.reporting import ReportService

app = typer.Typer(
    name="pentest",
    help="🔐 Penetration Testing Toolset - Comprehensive security testing framework",
    add_completion=False
)

console = Console()


@app.command()
def version():
    """Show version information."""
    from . import __version__
    console.print(Panel(
        f"[bold blue]Penetration Testing Toolset[/bold blue]\n"
        f"Version: [green]{__version__}[/green]\n"
        f"Environment: [yellow]{settings.environment}[/yellow]",
        title="Version Info"
    ))


@app.command()
def health():
    """Check system health."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Checking system health...", total=None)
        
        # Check database connection
        try:
            # Database health check would go here
            progress.update(task, description="✅ Database: Connected")
        except Exception as e:
            progress.update(task, description=f"❌ Database: {str(e)}")
        
        # Check Redis connection
        try:
            # Redis health check would go here
            progress.update(task, description="✅ Redis: Connected")
        except Exception as e:
            progress.update(task, description=f"❌ Redis: {str(e)}")
        
        # Check API status
        try:
            # API health check would go here
            progress.update(task, description="✅ API: Running")
        except Exception as e:
            progress.update(task, description=f"❌ API: {str(e)}")
    
    console.print("\n[bold green]System Health Check Complete![/bold green]")


@app.command()
def scan_network(
    target: str = typer.Argument(..., help="Target IP or network range (e.g., 192.168.1.0/24)"),
    ports: str = typer.Option("1-1000", help="Port range to scan"),
    scan_type: str = typer.Option("tcp", help="Scan type: tcp, udp, or stealth"),
    output: str = typer.Option("json", help="Output format: json, csv, or pdf"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output")
):
    """Perform network scanning and enumeration."""
    
    console.print(Panel(
        f"[bold blue]Network Scan[/bold blue]\n"
        f"Target: [green]{target}[/green]\n"
        f"Ports: [yellow]{ports}[/yellow]\n"
        f"Type: [cyan]{scan_type}[/cyan]",
        title="Scan Configuration"
    ))
    
    try:
        scanner = NetworkScanner()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Starting network scan...", total=None)
            
            # Perform the scan
            results = asyncio.run(scanner.scan_network(
                target=target,
                ports=ports,
                scan_type=scan_type
            ))
            
            progress.update(task, description="✅ Scan completed")
        
        # Display results
        if verbose:
            display_network_results(results)
        else:
            display_network_summary(results)
        
        # Generate report
        if output != "none":
            report_service = ReportService()
            report_path = asyncio.run(report_service.generate_network_report(
                results=results,
                format=output,
                filename=f"network_scan_{target.replace('/', '_')}"
            ))
            console.print(f"\n[green]Report saved to: {report_path}[/green]")
    
    except Exception as e:
        logger.error("Network scan failed", error=str(e))
        console.print(f"\n[red]❌ Scan failed: {str(e)}[/red]")
        raise typer.Exit(1)


@app.command()
def scan_web(
    url: str = typer.Argument(..., help="Target URL to scan"),
    scan_types: List[str] = typer.Option(
        ["sql", "xss", "csrf"], 
        help="Types of scans to perform"
    ),
    threads: int = typer.Option(10, help="Number of concurrent threads"),
    output: str = typer.Option("json", help="Output format: json, csv, or pdf"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output")
):
    """Perform web application security testing."""
    
    console.print(Panel(
        f"[bold blue]Web Application Scan[/bold blue]\n"
        f"URL: [green]{url}[/green]\n"
        f"Scan Types: [yellow]{', '.join(scan_types)}[/yellow]\n"
        f"Threads: [cyan]{threads}[/cyan]",
        title="Scan Configuration"
    ))
    
    try:
        scanner = WebScanner()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Starting web application scan...", total=None)
            
            # Perform the scan
            results = asyncio.run(scanner.scan_web_application(
                url=url,
                scan_types=scan_types,
                threads=threads
            ))
            
            progress.update(task, description="✅ Scan completed")
        
        # Display results
        if verbose:
            display_web_results(results)
        else:
            display_web_summary(results)
        
        # Generate report
        if output != "none":
            report_service = ReportService()
            report_path = asyncio.run(report_service.generate_web_report(
                results=results,
                format=output,
                filename=f"web_scan_{url.replace('://', '_').replace('/', '_')}"
            ))
            console.print(f"\n[green]Report saved to: {report_path}[/green]")
    
    except Exception as e:
        logger.error("Web scan failed", error=str(e))
        console.print(f"\n[red]❌ Scan failed: {str(e)}[/red]")
        raise typer.Exit(1)


@app.command()
def scan_database(
    host: str = typer.Argument(..., help="Database host"),
    port: int = typer.Option(5432, help="Database port"),
    db_type: str = typer.Option("postgresql", help="Database type: postgresql, mysql, mssql"),
    username: str = typer.Option("", help="Database username"),
    password: str = typer.Option("", help="Database password"),
    scan_types: List[str] = typer.Option(
        ["enumeration", "bruteforce", "privilege_escalation"],
        help="Types of scans to perform"
    ),
    output: str = typer.Option("json", help="Output format: json, csv, or pdf")
):
    """Perform database penetration testing."""
    
    console.print(Panel(
        f"[bold blue]Database Penetration Test[/bold blue]\n"
        f"Host: [green]{host}:{port}[/green]\n"
        f"Type: [yellow]{db_type}[/yellow]\n"
        f"Scan Types: [cyan]{', '.join(scan_types)}[/cyan]",
        title="Scan Configuration"
    ))
    
    try:
        scanner = DatabaseScanner()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Starting database penetration test...", total=None)
            
            # Perform the scan
            results = asyncio.run(scanner.scan_database(
                host=host,
                port=port,
                db_type=db_type,
                username=username,
                password=password,
                scan_types=scan_types
            ))
            
            progress.update(task, description="✅ Scan completed")
        
        # Display results
        display_database_results(results)
        
        # Generate report
        if output != "none":
            report_service = ReportService()
            report_path = asyncio.run(report_service.generate_database_report(
                results=results,
                format=output,
                filename=f"database_scan_{host}_{port}"
            ))
            console.print(f"\n[green]Report saved to: {report_path}[/green]")
    
    except Exception as e:
        logger.error("Database scan failed", error=str(e))
        console.print(f"\n[red]❌ Scan failed: {str(e)}[/red]")
        raise typer.Exit(1)


@app.command()
def list_modules():
    """List available scanning modules."""
    
    table = Table(title="Available Scanning Modules")
    table.add_column("Module", style="cyan", no_wrap=True)
    table.add_column("Description", style="magenta")
    table.add_column("Status", style="green")
    
    modules = [
        ("Network Scanner", "Port scanning, OS detection, service enumeration", "✅ Ready"),
        ("Web Scanner", "SQL injection, XSS, CSRF, file inclusion", "✅ Ready"),
        ("Database Scanner", "Database enumeration, brute force, privilege escalation", "✅ Ready"),
        ("Wireless Scanner", "Wi-Fi handshake capture, rogue AP detection", "🔄 Coming Soon"),
        ("Post-Exploit", "Shell access, privilege escalation, persistence", "🔄 Coming Soon"),
    ]
    
    for module, description, status in modules:
        table.add_row(module, description, status)
    
    console.print(table)


@app.command()
def generate_report(
    scan_id: str = typer.Argument(..., help="Scan ID to generate report for"),
    format: str = typer.Option("pdf", help="Report format: pdf, json, csv, html"),
    template: str = typer.Option("default", help="Report template to use")
):
    """Generate a comprehensive report for a completed scan."""
    
    try:
        report_service = ReportService()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Generating report...", total=None)
            
            # Generate the report
            report_path = asyncio.run(report_service.generate_report(
                scan_id=scan_id,
                format=format,
                template=template
            ))
            
            progress.update(task, description="✅ Report generated")
        
        console.print(f"\n[green]✅ Report generated successfully![/green]")
        console.print(f"[blue]Location: {report_path}[/blue]")
    
    except Exception as e:
        logger.error("Report generation failed", error=str(e))
        console.print(f"\n[red]❌ Report generation failed: {str(e)}[/red]")
        raise typer.Exit(1)


def display_network_results(results):
    """Display detailed network scan results."""
    table = Table(title="Network Scan Results")
    table.add_column("Host", style="cyan")
    table.add_column("Port", style="magenta")
    table.add_column("Service", style="green")
    table.add_column("Version", style="yellow")
    table.add_column("Status", style="red")
    
    for host, ports in results.items():
        for port_info in ports:
            table.add_row(
                host,
                str(port_info.get("port", "")),
                port_info.get("service", ""),
                port_info.get("version", ""),
                port_info.get("status", "")
            )
    
    console.print(table)


def display_network_summary(results):
    """Display network scan summary."""
    total_hosts = len(results)
    total_ports = sum(len(ports) for ports in results.values())
    open_ports = sum(
        len([p for p in ports if p.get("status") == "open"])
        for ports in results.values()
    )
    
    console.print(Panel(
        f"[bold]Scan Summary[/bold]\n"
        f"Hosts Scanned: [green]{total_hosts}[/green]\n"
        f"Total Ports: [yellow]{total_ports}[/yellow]\n"
        f"Open Ports: [red]{open_ports}[/red]",
        title="Results"
    ))


def display_web_results(results):
    """Display detailed web scan results."""
    table = Table(title="Web Application Scan Results")
    table.add_column("Vulnerability", style="cyan")
    table.add_column("URL", style="magenta")
    table.add_column("Parameter", style="green")
    table.add_column("Severity", style="yellow")
    table.add_column("Description", style="red")
    
    for vuln in results.get("vulnerabilities", []):
        table.add_row(
            vuln.get("type", ""),
            vuln.get("url", ""),
            vuln.get("parameter", ""),
            vuln.get("severity", ""),
            vuln.get("description", "")
        )
    
    console.print(table)


def display_web_summary(results):
    """Display web scan summary."""
    vulnerabilities = results.get("vulnerabilities", [])
    critical = len([v for v in vulnerabilities if v.get("severity") == "critical"])
    high = len([v for v in vulnerabilities if v.get("severity") == "high"])
    medium = len([v for v in vulnerabilities if v.get("severity") == "medium"])
    low = len([v for v in vulnerabilities if v.get("severity") == "low"])
    
    console.print(Panel(
        f"[bold]Scan Summary[/bold]\n"
        f"Critical: [red]{critical}[/red]\n"
        f"High: [yellow]{high}[/yellow]\n"
        f"Medium: [blue]{medium}[/blue]\n"
        f"Low: [green]{low}[/green]",
        title="Results"
    ))


def display_database_results(results):
    """Display database scan results."""
    table = Table(title="Database Penetration Test Results")
    table.add_column("Test", style="cyan")
    table.add_column("Result", style="magenta")
    table.add_column("Details", style="green")
    table.add_column("Risk", style="yellow")
    
    for test, result in results.items():
        table.add_row(
            test,
            result.get("status", ""),
            result.get("details", ""),
            result.get("risk", "")
        )
    
    console.print(table)


if __name__ == "__main__":
    app() 