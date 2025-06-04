# Project Luna

Luna is an offensive security automation framework. The current implementation
includes a Typer-based CLI with database initialization, recon wrappers,
CVE lookup, simple reporting utilities, and a lightweight fuzzer. Recon now
supports fetching Wayback Machine URLs and passive DNS records.

## Quickstart
```bash
pip install -e .
luna init
luna hunt example.com
luna fuzz https://example.com --wordlist params.txt
luna show-exploits CVE-2020-1234
luna report --output report.md
```
