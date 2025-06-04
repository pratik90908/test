# Project Luna

Luna is an offensive security automation framework. The current implementation
includes a Typer-based CLI with database initialization, recon wrappers,
CVE lookup, simple reporting utilities, and a lightweight fuzzer. Recon now
supports fetching Wayback Machine URLs and passive DNS records.

The `hunt` command only operates on domains listed in `targets.txt` to ensure
you have permission to test.

## Quickstart
```bash
pip install -e .
luna init
echo "example.com" > targets.txt
luna hunt example.com
luna fuzz https://example.com --wordlist params.txt
luna show-exploits CVE-2020-1234
luna report --output report.md
```
