from __future__ import annotations

import asyncio
from typing import Dict, List

import httpx


async def _request(client: httpx.AsyncClient, url: str, param: str) -> int:
    """Helper to send a GET request with a single parameter."""
    try:
        resp = await client.get(url, params={param: "test"})
        return resp.status_code
    except httpx.HTTPError:
        return 0


async def param_bruteforce(url: str, wordlist: List[str]) -> Dict[str, int]:
    """Bruteforce parameter names asynchronously returning status codes."""
    results: Dict[str, int] = {}
    async with httpx.AsyncClient(timeout=5) as client:
        tasks = [asyncio.create_task(_request(client, url, w)) for w in wordlist]
        for word, task in zip(wordlist, tasks):
            results[word] = await task
    return results


def detect_waf(status_codes: List[int]) -> bool:
    """Simple heuristic to guess if a WAF is present."""
    blocked = [code for code in status_codes if code in {403, 429}]
    return len(blocked) > len(status_codes) / 2

