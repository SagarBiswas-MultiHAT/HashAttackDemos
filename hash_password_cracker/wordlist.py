"""Wordlist helpers."""

from __future__ import annotations

from typing import Iterable


def iter_wordlist(path: str) -> Iterable[str]:
    """Yield cleaned, non-empty lines from a wordlist file."""
    with open(path, encoding="utf-8", errors="ignore") as handle:
        for line in handle:
            word = line.strip()
            if word:
                yield word
