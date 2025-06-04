import asyncio
import os
import typer

from pathlib import Path

from luna import recon, scanner, fuzzer, exploits
from luna.db import init_db
from luna.reporting import save_report
from luna.utils import load_targets

app = typer.Typer(help="Luna Offensive Security Automation Framework")

@app.command()
def init(db_url: str = typer.Option(None, help="PostgreSQL connection URL")):
    """Initialize database and folders."""
    url = db_url or os.getenv("LUNA_DB_URL", "postgresql://localhost/luna")
    init_db(url)
    typer.echo(f"Initialized Luna environment with DB {url}")

@app.command()
def hunt(
    target: str,
    depth: int = 1,
    threads: int = 10,
    targets_file: Path = typer.Option(Path("targets.txt"), help="Scope file"),
):
    """Run full hunt against a target."""
    allowed = load_targets(targets_file)
    if not allowed or target not in allowed:
        typer.echo(f"{target} not in {targets_file}", err=True)
        raise typer.Exit(1)
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

    urls = asyncio.run(recon.wayback_urls(target))
    typer.echo(f"{len(urls)} wayback URLs found")

    pdns = asyncio.run(recon.passive_dns(target))
    typer.echo(f"{len(pdns)} passive DNS domains found")

    results = asyncio.run(scanner.fetch_cves(target))
    typer.echo(f"Fetched {len(results)} CVEs for {target}")


@app.command()
def fuzz(url: str, wordlist: Path = typer.Option(Path("params.txt"))):
    """Bruteforce parameter names on a URL."""
    if not wordlist.exists():
        typer.echo(f"Wordlist {wordlist} not found")
        raise typer.Exit(1)
    words = [line.strip() for line in wordlist.read_text().splitlines() if line.strip()]
    typer.echo(f"Fuzzing {url} with {len(words)} parameters")
    results = asyncio.run(fuzzer.param_bruteforce(url, words))
    waf = fuzzer.detect_waf(list(results.values()))
    for param, code in results.items():
        typer.echo(f"{param}: {code}")
    if waf:
        typer.echo("Possible WAF detected")


@app.command()
def show_exploits(cve: str):
    """Fetch exploits for a given CVE."""
    results = asyncio.run(exploits.fetch_exploits(cve))
    typer.echo(f"{len(results)} exploits found for {cve}")
    for item in results:
        typer.echo(f"- {item.get('id')}")

@app.command()
def report(format: str = typer.Option("md", help="Report format"), output: Path = typer.Option(Path("report.md"), help="Output file")):
    """Generate report."""
    content = "# Luna Report\n\nResults go here."
    save_report(content, output)
    typer.echo(f"Report saved to {output} as {format}")

if __name__ == "__main__":
    app()
