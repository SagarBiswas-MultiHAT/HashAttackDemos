"""Educational demo: build a tiny rainbow table from a small dictionary.

This demonstrates why unsalted, fast hashes (like MD5) are dangerous.
"""

from __future__ import annotations

import hashlib
from typing import Iterable


def build_rainbow_table(words: Iterable[str]) -> dict[str, str]:
    """Return a mapping of md5_hash -> plaintext."""
    table: dict[str, str] = {}
    for word in words:
        md5_hash = hashlib.md5(word.encode("utf-8")).hexdigest()
        table[md5_hash] = word
    return table


def main() -> None:
    dictionary = ["123456", "password", "qwerty", "letmein", "admin"]

    print("Building rainbow table from a tiny dictionary...")
    table = build_rainbow_table(dictionary)

    print("\nRainbow table entries (md5 -> plaintext):")
    for md5_hash, word in table.items():
        print(f"{md5_hash} : {word}")

    stolen_password = "qwerty"
    stolen_hash = hashlib.md5(stolen_password.encode("utf-8")).hexdigest()

    print("\nSimulated stolen hash:")
    print(stolen_hash)

    recovered = table.get(stolen_hash)
    if recovered:
        print(f"\nPassword cracked! Plaintext is: {recovered}")
    else:
        print("\nPassword not found in the rainbow table.")

    print("\nKey lesson: MD5 is fast and unsalted, so rainbow tables can crack it quickly.")


if __name__ == "__main__":
    main()
