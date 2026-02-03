"""Educational demo: salted vs unsalted hashes.

This is not a password storage recommendation. It only shows why salts matter.
"""

from __future__ import annotations

import hashlib
import os


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    password = "password123"

    unsalted_1 = sha256_hex(password.encode("utf-8"))
    unsalted_2 = sha256_hex(password.encode("utf-8"))

    salt_a = os.urandom(16)
    salt_b = os.urandom(16)

    salted_1 = sha256_hex(salt_a + password.encode("utf-8"))
    salted_2 = sha256_hex(salt_b + password.encode("utf-8"))

    print("Password:", password)
    print("\nUnsalted hash 1:")
    print(unsalted_1)
    print("Unsalted hash 2:")
    print(unsalted_2)

    print("\nSalted hash 1 (salt A):")
    print(salted_1)
    print("Salted hash 2 (salt B):")
    print(salted_2)

    print("\nKey lesson: salting makes identical passwords hash differently.")


if __name__ == "__main__":
    main()
