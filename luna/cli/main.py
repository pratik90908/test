import asyncio
import os
import typer

from pathlib import Path

from luna import recon, scanner
from luna.db import init_db
from luna.reporting import save_report

app = typer.Typer(help="Luna Offensive Security Automation Framework")

@app.command()
def init(db_url: str = typer.Option(None, help="PostgreSQL connection URL")):
    """Initialize database and folders."""
    url = db_url or os.getenv("LUNA_DB_URL", "postgresql://localhost/luna")
    init_db(url)
    typer.echo(f"Initialized Luna environment with DB {url}")

@app.command()
def hunt(target: str, depth: int = 1, threads: int = 10):
    """Run full hunt against a target."""
    typer.echo(f"Starting hunt on {target} depth={depth} threads={threads}")
    try:
        subs = recon.enum_subdomains(target)
        typer.echo(f"{len(subs)} subdomains found")
    except RuntimeError as exc:
        typer.echo(f"Subdomain enumeration failed: {exc}")
        subs = []

    for sub in subs:
        typer.echo(f"- {sub}")

    try:
        ports = recon.port_scan(target)
        typer.echo(f"Open ports: {ports}")
    except RuntimeError as exc:
        typer.echo(f"Port scan failed: {exc}")

    results = asyncio.run(scanner.fetch_cves(target))
    typer.echo(f"Fetched {len(results)} CVEs for {target}")

@app.command()
def report(format: str = typer.Option("md", help="Report format"), output: Path = typer.Option(Path("report.md"), help="Output file")):
    """Generate report."""
    content = "# Luna Report\n\nResults go here."
    save_report(content, output)
    typer.echo(f"Report saved to {output} as {format}")

if __name__ == "__main__":
    app()
