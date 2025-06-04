"""Utility helpers for Project Luna."""

from __future__ import annotations

from pathlib import Path
from typing import List


def load_targets(path: Path = Path("targets.txt")) -> List[str]:
    """Return allowed targets listed in the given file."""
    if not path.exists():
        return []
    return [line.strip() for line in path.read_text().splitlines() if line.strip()]

