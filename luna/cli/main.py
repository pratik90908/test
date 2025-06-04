import typer

app = typer.Typer(help="Luna Offensive Security Automation Framework")

@app.command()
def init(db_url: str = typer.Option("postgresql://localhost/luna", help="PostgreSQL connection URL")):
    """Initialize database and folders."""
    typer.echo(f"Initializing Luna environment with DB {db_url}")

@app.command()
def hunt(target: str, depth: int = 1, threads: int = 10):
    """Run full hunt against a target."""
    typer.echo(f"Starting hunt on {target} depth={depth} threads={threads}")

@app.command()
def report(format: str = typer.Option("pdf", help="Report format")):
    """Generate report."""
    typer.echo(f"Generating report as {format}")

if __name__ == "__main__":
    app()
