"""Educational demo: why rainbow tables fail against Argon2id.

Argon2id uses a random salt, so the same password produces different hashes.
"""

from __future__ import annotations

from argon2 import PasswordHasher


def main() -> None:
    ph = PasswordHasher(time_cost=3, memory_cost=65536, parallelism=4)

    password = "password123"
    hash1 = ph.hash(password)
    hash2 = ph.hash(password)

    print("Password:", password)
    print("\nHash 1:")
    print(hash1)
    print("\nHash 2:")
    print(hash2)

    print("\nEven though the password is the same, the hashes are different.")
    print("That's the salt doing its job, which breaks rainbow tables.")


if __name__ == "__main__":
    main()
