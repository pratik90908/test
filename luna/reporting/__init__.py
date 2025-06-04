from __future__ import annotations

from pathlib import Path


def save_report(content: str, path: Path) -> None:
    """Save given Markdown content to a file."""
    path.write_text(content)
