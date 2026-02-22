"""Tests for filename sanitization and URL name helpers."""
import pytest
from ctf_scraper import UniversalCTFScraper


@pytest.mark.parametrize("raw, expected", [
    ("Normal Name",        "Normal Name"),
    ("Web/Exploitation",   "Web_Exploitation"),       # / → _
    ("Pwn:Buffer",         "Pwn_Buffer"),              # : → _
    ('Say "Hello"',        'Say _Hello_'),             # " → _
    ("File|Pipe",          "File_Pipe"),               # | → _
    ("..hidden",           "hidden"),                  # leading dots stripped
    ("  spaces  ",         "spaces"),                  # leading/trailing spaces
    ("",                   "unnamed"),                 # empty → fallback
    ("A?B*C",              "A_B_C"),                   # ? * → _
    ("Path\\File",         "Path_File"),               # backslash → _
])
def test_sanitize_filename(raw, expected):
    assert UniversalCTFScraper._sanitize_filename(raw) == expected


def test_sanitize_filename_unicode():
    """Unicode characters should pass through unchanged."""
    result = UniversalCTFScraper._sanitize_filename("Crédits & Réseaux")
    assert "Crédits" in result
    assert "&" in result


def test_sanitize_url_name(tmp_path):
    """_sanitize_url_name converts to lowercase hyphenated slug."""
    scraper = UniversalCTFScraper.__new__(UniversalCTFScraper)
    assert scraper._sanitize_url_name("SQL Injection 101") == "sql-injection-101"
    assert scraper._sanitize_url_name("RSA_Baby") == "rsa-baby"
    assert scraper._sanitize_url_name("XSS") == "xss"
