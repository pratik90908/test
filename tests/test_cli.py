from typer.testing import CliRunner
from luna.cli.main import app
import os

runner = CliRunner()


def test_init():
    result = runner.invoke(app, ["init", "--db-url", "sqlite:///test.db"])
    assert result.exit_code == 0
    assert "Initialized Luna" in result.stdout

def test_hunt(monkeypatch, tmp_path):
    targets = tmp_path / "targets.txt"
    targets.write_text("example.com\n")
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr("luna.recon.enum_subdomains", lambda d: [])
    monkeypatch.setattr("luna.recon.port_scan", lambda t: [])

    async def _async_noop(*args, **kwargs):
        return []

    monkeypatch.setattr("luna.recon.wayback_urls", _async_noop)
    monkeypatch.setattr("luna.recon.passive_dns", _async_noop)
    monkeypatch.setattr("luna.scanner.fetch_cves", _async_noop)
    result = runner.invoke(app, ["hunt", "example.com"])
    assert result.exit_code == 0
    assert "Starting hunt" in result.stdout

def test_report():
    result = runner.invoke(app, ["report", "--output", "test.md"])
    assert result.exit_code == 0
    assert "Report saved" in result.stdout


def test_hunt_out_of_scope(tmp_path):
    (tmp_path / "targets.txt").write_text("allowed.com\n")
    runner = CliRunner()
    os.chdir(tmp_path)
    result = runner.invoke(app, ["hunt", "example.com"], env={"PYTHONUNBUFFERED": "1"})
    assert result.exit_code == 1
    assert "not in" in result.stdout


def test_fuzz(tmp_path):
    wordlist = tmp_path / "params.txt"
    wordlist.write_text("id\nq\n")
    result = runner.invoke(app, ["fuzz", "https://example.com", "--wordlist", str(wordlist)])
    assert result.exit_code == 0
    assert "Fuzzing" in result.stdout


def test_exploits(monkeypatch):
    async def _async_noop(*args, **kwargs):
        return [{"id": "EXP"}]

    monkeypatch.setattr("luna.exploits.fetch_exploits", _async_noop)
    result = runner.invoke(app, ["show-exploits", "CVE-0000"])
    assert result.exit_code == 0
    assert "1 exploits found" in result.stdout
