from __future__ import annotations

import shutil
import subprocess
from typing import List, Set

from Wappalyzer import Wappalyzer, WebPage


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
    wappalyzer = Wappalyzer.latest()
    webpage = WebPage.new_from_url(url)
    return set(wappalyzer.analyze(webpage))
