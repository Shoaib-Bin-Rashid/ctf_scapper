"""Tests for platform detection and RateLimiter."""
import time
import pytest
from unittest.mock import MagicMock, patch
from ctf_scraper import UniversalCTFScraper, RateLimiter


# ── Platform Detection ────────────────────────────────────────────────────────

def _scraper_for(tmp_path, url):
    return UniversalCTFScraper(
        url=url,
        cookies_str=None,
        output_dir=str(tmp_path),
    )


def test_detect_picoctf_by_domain(tmp_path):
    scraper = _scraper_for(tmp_path, "https://play.picoctf.org/practice")
    with patch.object(scraper.session, 'get') as mock_get:
        result = scraper.detect_platform()
    assert result == 'picoctf'
    mock_get.assert_not_called()   # domain match is instant — no network needed


def test_detect_ctfd_by_api_response(tmp_path):
    scraper = _scraper_for(tmp_path, "https://ctf.example.com/challenges")
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.content = b'{"success": true, "data": []}'
    mock_resp.json.return_value = {"success": True, "data": []}
    with patch.object(scraper.session, 'get', return_value=mock_resp):
        result = scraper.detect_platform()
    assert result == 'ctfd'


def test_detect_unknown_when_api_fails(tmp_path):
    scraper = _scraper_for(tmp_path, "https://unknown-platform.io/challenges")
    mock_resp = MagicMock()
    mock_resp.status_code = 404
    mock_resp.content = b''
    mock_resp.json.side_effect = ValueError("no json")
    with patch.object(scraper.session, 'get', return_value=mock_resp):
        result = scraper.detect_platform()
    assert result == 'unknown'


def test_detect_ctfd_uses_correct_endpoint(tmp_path):
    """Ensure detection probes /api/v1/challenges, not some other path."""
    scraper = _scraper_for(tmp_path, "https://ctf.example.com/challenges")
    called_urls = []

    def fake_get(url, **kwargs):
        called_urls.append(url)
        resp = MagicMock()
        resp.status_code = 200
        resp.content = b'{"success":true,"data":[]}'
        resp.json.return_value = {"success": True, "data": []}
        return resp

    with patch.object(scraper.session, 'get', side_effect=fake_get):
        scraper.detect_platform()

    assert any('/api/v1/challenges' in u for u in called_urls)


# ── RateLimiter ───────────────────────────────────────────────────────────────

def test_rate_limiter_zero_is_instant():
    """rate_limit=0 (disabled) should not block."""
    limiter = RateLimiter(0)
    start = time.monotonic()
    for _ in range(10):
        limiter.wait()
    assert time.monotonic() - start < 0.1


def test_rate_limiter_enforces_interval():
    """rate_limit=10 req/sec → each call ~0.1s apart."""
    limiter = RateLimiter(10)
    start = time.monotonic()
    for _ in range(3):
        limiter.wait()
    elapsed = time.monotonic() - start
    # 3 calls at 10/sec → at least ~0.2s (2 intervals), with some tolerance
    assert elapsed >= 0.15


def test_version_string():
    from ctf_scraper import __version__
    parts = __version__.split('.')
    assert len(parts) == 3
    assert all(p.isdigit() for p in parts)
