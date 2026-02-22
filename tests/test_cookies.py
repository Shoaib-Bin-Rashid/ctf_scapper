"""Tests for cookie parsing — string, file, and env-var methods."""
import os
import pytest
from unittest.mock import patch
from pathlib import Path
from ctf_scraper import UniversalCTFScraper


def _make_scraper(tmp_path, cookies_str=None):
    """Instantiate a scraper pointed at a dummy URL without network calls."""
    return UniversalCTFScraper(
        url="https://ctf.example.com/challenges",
        cookies_str=cookies_str,
        output_dir=str(tmp_path),
    )


def test_parse_simple_cookies(tmp_path):
    scraper = _make_scraper(tmp_path, "session=abc123; csrftoken=xyz")
    assert scraper.cookies == {"session": "abc123", "csrftoken": "xyz"}


def test_parse_cookies_with_spaces(tmp_path):
    scraper = _make_scraper(tmp_path, "  session = abc ; token = def  ")
    assert scraper.cookies["session"] == "abc"
    assert scraper.cookies["token"] == "def"


def test_parse_cookies_value_with_equals(tmp_path):
    """Cookie values can contain '=' — only split on the first one."""
    scraper = _make_scraper(tmp_path, "token=abc=def==")
    assert scraper.cookies["token"] == "abc=def=="


def test_parse_cookies_from_file(tmp_path):
    cookie_file = tmp_path / "cookies.txt"
    cookie_file.write_text("session=file_cookie; cf_clearance=yyy")
    scraper = _make_scraper(tmp_path, f"@{cookie_file}")
    assert scraper.cookies["session"] == "file_cookie"
    assert scraper.cookies["cf_clearance"] == "yyy"


def test_parse_cookies_file_not_found_exits(tmp_path):
    with pytest.raises(SystemExit):
        _make_scraper(tmp_path, "@/nonexistent/path/cookies.txt")


def test_no_cookies_gives_empty_dict(tmp_path):
    scraper = _make_scraper(tmp_path, None)
    assert scraper.cookies == {}


def test_cookies_set_on_session(tmp_path):
    """Parsed cookies must be applied to the requests.Session."""
    scraper = _make_scraper(tmp_path, "session=s1; token=t1")
    assert scraper.session.cookies.get("session") == "s1"
    assert scraper.session.cookies.get("token") == "t1"
