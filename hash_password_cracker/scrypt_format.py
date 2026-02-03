"""Scrypt hashing helpers with a portable storage format."""

from __future__ import annotations

import hashlib
import hmac
import os
import re
from dataclasses import dataclass


@dataclass(frozen=True)
class ScryptParams:
    n: int = 16384
    r: int = 8
    p: int = 1
    dklen: int = 32


DEFAULT_SCRYPT_PARAMS = ScryptParams()

_SCRYPT_FULL_RE = re.compile(r"^n=(\d+),r=(\d+),p=(\d+)\$([0-9a-fA-F]+)\$([0-9a-fA-F]+)$")


def derive_scrypt_key(password: str, salt: bytes, params: ScryptParams) -> bytes:
    return hashlib.scrypt(
        password.encode("utf-8"),
        salt=salt,
        n=params.n,
        r=params.r,
        p=params.p,
        dklen=params.dklen,
    )


def encode_scrypt_hash(
    params: ScryptParams,
    salt: bytes,
    key: bytes,
    include_params: bool = True,
) -> str:
    salt_hex = salt.hex()
    key_hex = key.hex()
    if include_params:
        return f"n={params.n},r={params.r},p={params.p}${salt_hex}${key_hex}"
    return f"{salt_hex}:{key_hex}"


def parse_scrypt_hash(
    hash_value: str,
    default_params: ScryptParams = DEFAULT_SCRYPT_PARAMS,
) -> tuple[ScryptParams, bytes, bytes]:
    """Parse supported scrypt hash formats.

    Supported formats:
    - n=<N>,r=<r>,p=<p>$<salt_hex>$<hash_hex>
    - <salt_hex>:<hash_hex> (uses default_params)
    """
    candidate = hash_value.strip()

    full_match = _SCRYPT_FULL_RE.match(candidate)
    if full_match:
        n_str, r_str, p_str, salt_hex, key_hex = full_match.groups()
        key_bytes = bytes.fromhex(key_hex)
        params = ScryptParams(
            n=int(n_str),
            r=int(r_str),
            p=int(p_str),
            dklen=len(key_bytes),
        )
        return params, bytes.fromhex(salt_hex), key_bytes

    if ":" in candidate:
        salt_hex, key_hex = candidate.split(":", 1)
        key_bytes = bytes.fromhex(key_hex)
        params = ScryptParams(
            n=default_params.n,
            r=default_params.r,
            p=default_params.p,
            dklen=len(key_bytes),
        )
        return params, bytes.fromhex(salt_hex), key_bytes

    raise ValueError("Unsupported scrypt hash format.")


def hash_scrypt(
    password: str,
    params: ScryptParams = DEFAULT_SCRYPT_PARAMS,
    salt: bytes | None = None,
    include_params: bool = True,
) -> str:
    """Hash a password using scrypt and return an encoded string."""
    if salt is None:
        salt = os.urandom(16)
    key = derive_scrypt_key(password, salt, params)
    return encode_scrypt_hash(params, salt, key, include_params=include_params)


def verify_scrypt(
    password: str,
    hash_value: str,
    default_params: ScryptParams = DEFAULT_SCRYPT_PARAMS,
) -> bool:
    """Verify a password against a supported scrypt hash format."""
    try:
        params, salt, stored_key = parse_scrypt_hash(hash_value, default_params=default_params)
    except ValueError:
        return False

    derived_key = derive_scrypt_key(password, salt, params)
    return hmac.compare_digest(derived_key, stored_key)
