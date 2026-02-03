"""Attack helpers used by demo scripts."""

from __future__ import annotations

from typing import Callable

from .hashing import verify_argon2id, verify_bcrypt
from .scrypt_format import verify_scrypt
from .wordlist import iter_wordlist

VerifyFn = Callable[[str, str], bool]

SUPPORTED_ALGORITHMS: dict[str, VerifyFn] = {
    "argon2id": verify_argon2id,
    "bcrypt": verify_bcrypt,
    "scrypt": verify_scrypt,
}


def dictionary_attack(stored_hash: str, wordlist_path: str, algorithm: str) -> str | None:
    """Return the first password that verifies or None if not found."""
    verify = SUPPORTED_ALGORITHMS[algorithm]
    for password in iter_wordlist(wordlist_path):
        if verify(password, stored_hash):
            return password
    return None
