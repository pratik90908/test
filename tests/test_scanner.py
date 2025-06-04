import pytest
from luna.scanner import fetch_cves


@pytest.mark.asyncio
async def test_fetch_cves(httpx_mock):
    expected = [{"id": "CVE-0000"}]
    httpx_mock.add_response(json={"data": {"search": expected}})
    results = await fetch_cves("test")
    assert results == expected
