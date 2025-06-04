# Project Luna

Luna is an offensive security automation framework. The current implementation
includes a basic CLI with database initialization, recon wrappers, CVE lookup,
simple reporting utilities, and a lightweight fuzzer.

## Quickstart
```bash
pip install -e .
luna init
luna hunt example.com
luna fuzz https://example.com --wordlist params.txt
luna report --output report.md
```
