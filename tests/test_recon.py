import pytest
from luna.recon import passive_dns, wayback_urls


@pytest.mark.asyncio
async def test_passive_dns(httpx_mock):
    httpx_mock.add_response(json={"FDNS_A": ["1.1.1.1,foo.example.com"], "RDNS": []})
    result = await passive_dns("example.com")
    assert result == ["foo.example.com"]


@pytest.mark.asyncio
async def test_wayback_urls(httpx_mock):
    httpx_mock.add_response(json=[["original"], ["http://example.com/index"]])
    result = await wayback_urls("example.com")
    assert result == ["http://example.com/index"]
