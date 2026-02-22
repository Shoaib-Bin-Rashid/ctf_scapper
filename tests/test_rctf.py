"""Tests for rCTF + Mellivora detection and scraping helpers."""
import json
from unittest.mock import MagicMock, patch

import pytest

from ctf_scraper import UniversalCTFScraper, _html_to_text


# ---------------------------------------------------------------------------
# _html_to_text
# ---------------------------------------------------------------------------

def test_html_to_text_strips_tags():
    result = _html_to_text("<p>Hello <b>world</b></p>")
    assert "Hello" in result and "world" in result
    assert "<" not in result and ">" not in result


def test_html_to_text_plain_passthrough():
    assert _html_to_text("no html here") == "no html here"


def test_html_to_text_empty():
    assert _html_to_text("") == ""


def test_html_to_text_entities():
    result = _html_to_text("<p>a &amp; b</p>")
    assert "&amp;" not in result
    assert "a" in result and "b" in result


def test_html_to_text_nested():
    result = _html_to_text("<div><ul><li>item 1</li><li>item 2</li></ul></div>")
    assert "item 1" in result
    assert "item 2" in result


# ---------------------------------------------------------------------------
# detect_platform — rCTF
# ---------------------------------------------------------------------------

def _make_scraper(url="https://example.com"):
    return UniversalCTFScraper(url=url, output_dir="/tmp/test_out")


def _mock_response(status=200, json_data=None, raise_exc=None):
    resp = MagicMock()
    resp.status_code = status
    resp.json.return_value = json_data or {}
    if raise_exc:
        resp.raise_for_status.side_effect = raise_exc
    else:
        resp.raise_for_status.return_value = None
    return resp


def test_detect_platform_rctf(tmp_path):
    scraper = UniversalCTFScraper(url="https://ctf.redpwn.net", output_dir=str(tmp_path))
    rctf_resp = _mock_response(json_data={"kind": "goodChallenge", "data": []})
    ctfd_resp = _mock_response(raise_exc=Exception("not ctfd"))

    def side_effect(url, **kw):
        if "api/v1/challs" in url:
            return rctf_resp
        return ctfd_resp

    with patch.object(scraper.session, "get", side_effect=side_effect):
        platform = scraper.detect_platform()
    assert platform == "rctf"


def test_detect_platform_mellivora(tmp_path):
    scraper = UniversalCTFScraper(url="https://ctf.example.eu", output_dir=str(tmp_path))
    mellivora_resp = _mock_response(json_data=[{"title": "test", "category": "Web"}])
    fail_resp = _mock_response(status=404)

    def side_effect(url, **kw):
        if "api/challenges.php" in url:
            return mellivora_resp
        return fail_resp

    with patch.object(scraper.session, "get", side_effect=side_effect):
        platform = scraper.detect_platform()
    assert platform == "mellivora"


# ---------------------------------------------------------------------------
# _save_json_manifest
# ---------------------------------------------------------------------------

def test_save_json_manifest_creates_file(tmp_path):
    scraper = UniversalCTFScraper(
        url="https://ctf.example.com", output_dir=str(tmp_path))
    scraper._manifest = [
        {"name": "Test", "category": "Web", "points": 100}
    ]
    scraper._save_json_manifest()
    manifest_path = tmp_path / "index.json"
    assert manifest_path.exists()
    data = json.loads(manifest_path.read_text())
    assert data["total"] == 1
    assert data["challenges"][0]["name"] == "Test"
    assert "scraped_at" in data
    assert "version" in data
