"""Reusable hashing and demo utilities for this repository."""

from __future__ import annotations

from .attacks import SUPPORTED_ALGORITHMS, dictionary_attack
from .hashing import (
    DEFAULT_ARGON2_PARAMS,
    Argon2Params,
    hash_argon2id,
    hash_bcrypt,
    is_argon2_hash,
    is_bcrypt_hash,
    verify_argon2id,
    verify_bcrypt,
)
from .rainbow import (
    build_rainbow_table,
    is_md5_hex,
    load_rainbow_table,
    lookup_md5_hash,
    lookup_plaintext,
)
from .records import append_hash_record, build_hash_record
from .scrypt_format import (
    DEFAULT_SCRYPT_PARAMS,
    ScryptParams,
    encode_scrypt_hash,
    hash_scrypt,
    parse_scrypt_hash,
    verify_scrypt,
)
from .wordlist import iter_wordlist

__all__ = [
    "Argon2Params",
    "DEFAULT_ARGON2_PARAMS",
    "hash_argon2id",
    "verify_argon2id",
    "hash_bcrypt",
    "verify_bcrypt",
    "is_bcrypt_hash",
    "is_argon2_hash",
    "ScryptParams",
    "DEFAULT_SCRYPT_PARAMS",
    "hash_scrypt",
    "verify_scrypt",
    "parse_scrypt_hash",
    "encode_scrypt_hash",
    "build_rainbow_table",
    "load_rainbow_table",
    "lookup_md5_hash",
    "lookup_plaintext",
    "is_md5_hex",
    "dictionary_attack",
    "SUPPORTED_ALGORITHMS",
    "iter_wordlist",
    "build_hash_record",
    "append_hash_record",
]
