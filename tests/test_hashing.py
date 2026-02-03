from __future__ import annotations

from hash_password_cracker import (
    DEFAULT_SCRYPT_PARAMS,
    Argon2Params,
    ScryptParams,
    hash_argon2id,
    hash_bcrypt,
    hash_scrypt,
    is_argon2_hash,
    is_bcrypt_hash,
    verify_argon2id,
    verify_bcrypt,
    verify_scrypt,
)


def test_argon2_roundtrip():
    params = Argon2Params(
        time_cost=1,
        memory_cost=1024,
        parallelism=1,
        hash_len=16,
        salt_len=16,
    )
    hashed = hash_argon2id("password123", params)
    assert is_argon2_hash(hashed)
    assert verify_argon2id("password123", hashed)
    assert not verify_argon2id("wrong", hashed)
    assert not is_argon2_hash("argon2id$v=19$bad")


def test_bcrypt_roundtrip():
    hashed = hash_bcrypt("password123", rounds=4)
    assert is_bcrypt_hash(hashed)
    assert verify_bcrypt("password123", hashed)
    assert not verify_bcrypt("wrong", hashed)
    assert not is_bcrypt_hash("$2b$12$...")


def test_scrypt_roundtrip_with_params():
    params = ScryptParams(n=1024, r=8, p=1, dklen=16)
    salt = bytes.fromhex("00" * 16)
    hashed = hash_scrypt("password123", params=params, salt=salt, include_params=True)
    assert verify_scrypt("password123", hashed, default_params=params)
    assert not verify_scrypt("wrong", hashed, default_params=params)


def test_scrypt_roundtrip_legacy_format():
    salt = bytes.fromhex("11" * 16)
    hashed = hash_scrypt(
        "password123",
        params=DEFAULT_SCRYPT_PARAMS,
        salt=salt,
        include_params=False,
    )
    assert verify_scrypt("password123", hashed)
    assert not verify_scrypt("wrong", hashed)
