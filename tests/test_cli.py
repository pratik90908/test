from typer.testing import CliRunner
from luna.cli.main import app

runner = CliRunner()


def test_init():
    result = runner.invoke(app, ["init"])
    assert result.exit_code == 0
    assert "Initializing" in result.stdout

def test_hunt():
    result = runner.invoke(app, ["hunt", "example.com"])
    assert result.exit_code == 0
    assert "Starting hunt" in result.stdout

def test_report():
    result = runner.invoke(app, ["report"])
    assert result.exit_code == 0
    assert "Generating report" in result.stdout
