from __future__ import annotations

import shutil
import subprocess
from typing import List, Set

import httpx

from wappalyzer import analyze


def enum_subdomains(domain: str) -> List[str]:
    """Enumerate subdomains using subfinder if available."""
    if not shutil.which("subfinder"):
        raise RuntimeError("subfinder not installed")
    proc = subprocess.run(
        ["subfinder", "-d", domain, "-silent"],
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip())
    return [line.strip() for line in proc.stdout.splitlines() if line.strip()]


def port_scan(target: str) -> List[int]:
    """Run a basic port scan using rustscan if available."""
    if not shutil.which("rustscan"):
        raise RuntimeError("rustscan not installed")
    proc = subprocess.run(
        ["rustscan", "-a", target, "--ulimit", "5000"],
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip())
    ports: List[int] = []
    for line in proc.stdout.splitlines():
        if "/tcp" in line and "Open" in line:
            port = line.split("/")[0]
            if port.isdigit():
                ports.append(int(port))
    return ports


def tech_fingerprint(url: str) -> Set[str]:
    """Identify technologies used by a target URL."""
    result = analyze(url)
    return set(result.get(url, {}).keys())


async def wayback_urls(domain: str) -> List[str]:
    """Fetch historical URLs for a domain from the Wayback Machine."""
    url = "https://web.archive.org/cdx/search/cdx"
    params = {"url": f"*.{domain}/*", "output": "json", "fl": "original"}
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(url, params=params)
        resp.raise_for_status()
        data = resp.json()
    if not data:
        return []
    return [row[0] for row in data[1:]]


async def passive_dns(domain: str) -> List[str]:
    """Retrieve passive DNS records for a domain."""
    url = "https://dns.bufferover.run/dns"
    params = {"q": domain}
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(url, params=params)
        resp.raise_for_status()
        data = resp.json()
    hosts = data.get("FDNS_A", []) + data.get("RDNS", [])
    results = []
    for entry in hosts:
        parts = entry.split(",")
        if len(parts) > 1:
            results.append(parts[1])
    return list(set(results))
