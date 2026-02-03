"""Hashing helpers for Argon2id and bcrypt."""

from __future__ import annotations

import re
from dataclasses import dataclass

import bcrypt
from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError


@dataclass(frozen=True)
class Argon2Params:
    time_cost: int = 3
    memory_cost: int = 65536
    parallelism: int = 4
    hash_len: int = 32
    salt_len: int = 16


DEFAULT_ARGON2_PARAMS = Argon2Params()

_BCRYPT_RE = re.compile(r"^\$2[abxy]\$\d{2}\$[./A-Za-z0-9]{53}$")
_ARGON2_RE = re.compile(r"^\$argon2(id|i|d)\$v=\d+\$.*")


def is_bcrypt_hash(value: str) -> bool:
    """Return True if value appears to be a valid bcrypt hash string."""
    return bool(_BCRYPT_RE.match(value))


def is_argon2_hash(value: str) -> bool:
    """Return True if value appears to be a valid Argon2 hash string."""
    return bool(_ARGON2_RE.match(value))


def _argon2_hasher(params: Argon2Params) -> PasswordHasher:
    return PasswordHasher(
        time_cost=params.time_cost,
        memory_cost=params.memory_cost,
        parallelism=params.parallelism,
        hash_len=params.hash_len,
        salt_len=params.salt_len,
    )


def hash_argon2id(password: str, params: Argon2Params = DEFAULT_ARGON2_PARAMS) -> str:
    """Hash a password using Argon2id and return the encoded string."""
    return _argon2_hasher(params).hash(password)


def verify_argon2id(password: str, hash_value: str) -> bool:
    """Verify a password against an Argon2id encoded hash."""
    try:
        return PasswordHasher().verify(hash_value, password)
    except (VerificationError, InvalidHashError):
        return False


def hash_bcrypt(password: str, rounds: int = 12) -> str:
    """Hash a password using bcrypt and return the encoded string."""
    salt = bcrypt.gensalt(rounds=rounds)
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password.decode("utf-8")


def verify_bcrypt(password: str, hash_value: str) -> bool:
    """Verify a password against a bcrypt encoded hash."""
    if not is_bcrypt_hash(hash_value):
        return False
    try:
        return bcrypt.checkpw(password.encode("utf-8"), hash_value.encode("utf-8"))
    except ValueError:
        return False
