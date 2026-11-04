"""Allows `python -m praktikum_llm ...` in addition to the `llm` command."""
import sys

from praktikum_llm.cli import main

sys.exit(main())
