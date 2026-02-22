"""Tests for ScraperState — resume capability and set/list round-trip."""
import json
import pytest
from pathlib import Path
from ctf_scraper import ScraperState


def test_fresh_state_has_empty_sets(tmp_path):
    state = ScraperState(tmp_path / ".state.json")
    assert isinstance(state.state['completed_challenges'], set)
    assert isinstance(state.state['failed_challenges'], set)
    assert len(state.state['completed_challenges']) == 0


def test_mark_completed(tmp_path):
    state = ScraperState(tmp_path / ".state.json")
    state.mark_completed("42")
    assert state.is_completed("42")
    assert not state.is_completed("99")


def test_mark_failed(tmp_path):
    state = ScraperState(tmp_path / ".state.json")
    state.mark_failed("7")
    assert "7" in state.state['failed_challenges']


def test_completed_removes_from_failed(tmp_path):
    state = ScraperState(tmp_path / ".state.json")
    state.mark_failed("5")
    assert "5" in state.state['failed_challenges']
    state.mark_completed("5")
    assert "5" not in state.state['failed_challenges']
    assert state.is_completed("5")


def test_save_and_reload_preserves_sets(tmp_path):
    """Critical: JSON round-trip must restore sets, not leave them as lists."""
    state_file = tmp_path / ".state.json"
    state = ScraperState(state_file)
    state.mark_completed("1")
    state.mark_completed("2")
    state.mark_failed("3")

    # Reload from disk
    reloaded = ScraperState(state_file)
    assert isinstance(reloaded.state['completed_challenges'], set), \
        "completed_challenges must be a set after JSON reload, not a list"
    assert isinstance(reloaded.state['failed_challenges'], set), \
        "failed_challenges must be a set after JSON reload, not a list"
    assert reloaded.is_completed("1")
    assert reloaded.is_completed("2")
    assert "3" in reloaded.state['failed_challenges']


def test_reload_calls_add_without_error(tmp_path):
    """Regression: .add() on a reloaded state must not raise AttributeError."""
    state_file = tmp_path / ".state.json"
    state = ScraperState(state_file)
    state.mark_completed("10")

    reloaded = ScraperState(state_file)
    # This would raise AttributeError: 'list' has no .add() before the bug fix
    reloaded.mark_completed("20")
    assert reloaded.is_completed("20")


def test_corrupted_state_file_returns_fresh(tmp_path):
    state_file = tmp_path / ".state.json"
    state_file.write_text("not valid json {{{{")
    state = ScraperState(state_file)
    assert isinstance(state.state['completed_challenges'], set)
    assert len(state.state['completed_challenges']) == 0


def test_state_platform_stored(tmp_path):
    state_file = tmp_path / ".state.json"
    state = ScraperState(state_file)
    state.state['platform'] = 'ctfd'
    state.save()
    reloaded = ScraperState(state_file)
    assert reloaded.state['platform'] == 'ctfd'
