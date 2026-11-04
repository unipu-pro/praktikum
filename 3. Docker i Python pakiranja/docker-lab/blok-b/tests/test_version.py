"""Tests for reading the tool version from version.txt."""
from pathlib import Path

import llm

VERSION_FILE = Path(__file__).resolve().parent.parent / "version.txt"


def test_read_version_matches_version_file():
    assert llm.read_version() == VERSION_FILE.read_text(encoding="utf-8").strip()


def test_read_version_falls_back_when_file_is_missing(monkeypatch, tmp_path):
    monkeypatch.setattr(llm, "VERSION_FILE", tmp_path / "missing.txt")

    assert llm.read_version() == "0.0.0"
