"""Rainbow table helpers (MD5 demo only)."""

from __future__ import annotations

import hashlib
import json
import os
import string

from .wordlist import iter_wordlist


def build_rainbow_table(wordlist_path: str, out_file: str) -> None:
    """Build a rainbow table mapping md5 -> plaintext from a wordlist."""
    if not os.path.exists(wordlist_path):
        raise FileNotFoundError(f"Wordlist not found: {wordlist_path}")

    rainbow_table: dict[str, str] = {}
    for password in iter_wordlist(wordlist_path):
        md5_hash = hashlib.md5(password.encode("utf-8")).hexdigest()
        if md5_hash not in rainbow_table:
            rainbow_table[md5_hash] = password

    with open(out_file, "w", encoding="utf-8") as out:
        json.dump(rainbow_table, out, ensure_ascii=False, indent=2)


def load_rainbow_table(path: str) -> dict[str, str]:
    """Load a rainbow table JSON file."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Rainbow table not found: {path}")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def is_md5_hex(value: str) -> bool:
    """Return True if value looks like a 32-character hex MD5 string."""
    candidate = value.strip().lower()
    if len(candidate) != 32:
        return False
    return all(ch in string.hexdigits for ch in candidate)


def lookup_md5_hash(md5_hash: str, table: dict[str, str]) -> str | None:
    return table.get(md5_hash.lower())


def lookup_plaintext(plaintext: str, table: dict[str, str]) -> tuple[str | None, str | None]:
    """Return (hash, password) if plaintext is found or maps to a known hash."""
    computed_hash = hashlib.md5(plaintext.encode("utf-8")).hexdigest()
    mapped = table.get(computed_hash)
    if mapped:
        return computed_hash, mapped

    for h, pw in table.items():
        if pw == plaintext:
            return h, pw

    return None, None
