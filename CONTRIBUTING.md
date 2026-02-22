# Contributing to CTF Scraper

Thanks for your interest in contributing! Here's everything you need.

## Setup

```bash
git clone https://github.com/Shoaib-Bin-Rashid/ctf_scrapper.git
cd ctf_scrapper
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
pip install pytest
```

## Running Tests

```bash
pytest tests/ -v
```

All tests run without any network calls — everything is mocked.

## Making Changes

1. Fork the repo and create a branch: `git checkout -b feature/my-feature`
2. Make your changes
3. Add or update tests in `tests/` to cover your change
4. Run `pytest tests/ -v` — all tests must pass
5. Open a Pull Request against `main`

## Adding a New Platform

1. Add a detection branch in `UniversalCTFScraper.detect_platform()`
2. Add a `scrape_<platform>()` method following the same pattern as `scrape_ctfd()`
3. Wire it into `scrape()` dispatch
4. Add at least one detection test in `tests/test_platform.py`

## Reporting Bugs

Open an issue at [GitHub Issues](https://github.com/Shoaib-Bin-Rashid/ctf_scrapper/issues) with:
- The CTF platform URL (redacted if needed)
- The command you ran
- The full error output (run with `-v` for verbose logs)

## Author

**Shoaib Bin Rashid** — [github.com/Shoaib-Bin-Rashid](https://github.com/Shoaib-Bin-Rashid)
