"""The installed package reports the version from version.txt (read once, at build time)."""
from pathlib import Path

import praktikum_llm

VERSION_FILE = Path(__file__).resolve().parent.parent / "version.txt"


def test_package_version_matches_version_file():
    assert praktikum_llm.__version__ == VERSION_FILE.read_text(encoding="utf-8").strip()
