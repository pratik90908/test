from __future__ import annotations

from typing import List, Dict

import httpx


async def fetch_cves(query: str) -> List[Dict]:
    """Fetch vulnerabilities matching a query from the Vulners API."""
    url = "https://vulners.com/api/v3/search/lucene/"
    params = {"query": query}
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        data = response.json()
    return data.get("data", {}).get("search", [])
