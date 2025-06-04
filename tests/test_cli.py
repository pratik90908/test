from typer.testing import CliRunner
from luna.cli.main import app

runner = CliRunner()


def test_init():
    result = runner.invoke(app, ["init", "--db-url", "sqlite:///test.db"])
    assert result.exit_code == 0
    assert "Initialized Luna" in result.stdout

def test_hunt():
    result = runner.invoke(app, ["hunt", "example.com"])
    assert result.exit_code == 0
    assert "Starting hunt" in result.stdout

def test_report():
    result = runner.invoke(app, ["report", "--output", "test.md"])
    assert result.exit_code == 0
    assert "Report saved" in result.stdout
