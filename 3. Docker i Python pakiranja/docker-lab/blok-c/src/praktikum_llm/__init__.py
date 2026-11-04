"""Command line client for a local Ollama model."""
from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("praktikum-llm")
except PackageNotFoundError:  # running from a source tree that was never installed
    __version__ = "0.0.0"
