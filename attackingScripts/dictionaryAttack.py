"""Dictionary-based password verification demo."""

from __future__ import annotations

import argparse
import os

from hash_password_cracker import (
    SUPPORTED_ALGORITHMS,
    dictionary_attack,
    is_argon2_hash,
    is_bcrypt_hash,
)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

def resolve_path(user_input_path: str) -> str:
    return (
        user_input_path
        if os.path.isabs(user_input_path)
        else os.path.join(PROJECT_ROOT, user_input_path)
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Dictionary attack (verification-based).")
    parser.add_argument("--hash", dest="stored_hash", help="Stored hash to verify.")
    parser.add_argument("--wordlist", help="Path to wordlist file.")
    parser.add_argument(
        "--algorithm",
        choices=sorted(SUPPORTED_ALGORITHMS.keys()),
        help="Hash algorithm to verify against.",
    )
    return parser


def main() -> int:
    print("\n************** PASSWORD VERIFIER ******************\n")

    parser = build_parser()
    args = parser.parse_args()

    stored_hash = args.stored_hash or input("Enter the stored password hash: ").strip()
    wordlist_input = args.wordlist or input("Enter passwords file path: ").strip()
    algorithm = (
        args.algorithm
        or input("Choose algorithm (argon2id / bcrypt / scrypt): ").strip().lower()
    )

    if algorithm not in SUPPORTED_ALGORITHMS:
        print(f"\n[!] Unsupported algorithm: {algorithm}")
        print("Supported: argon2id, bcrypt, scrypt")
        return 2

    if algorithm == "bcrypt" and not is_bcrypt_hash(stored_hash):
        print("\n[!] Invalid bcrypt hash format.")
        print("Tip: provide the full $2b$... hash string, not a placeholder.")
        return 2

    if algorithm == "argon2id" and not is_argon2_hash(stored_hash):
        print("\n[!] Invalid Argon2id hash format.")
        print("Tip: in PowerShell, wrap hashes in single quotes to avoid $ expansion.")
        return 2

    wordlist_path = resolve_path(wordlist_input)

    try:
        found = dictionary_attack(stored_hash, wordlist_path, algorithm)
    except FileNotFoundError:
        print(f"\n[!] Error: File not found -> {wordlist_path}")
        return 1

    if found:
        print(f"\n[+] Password found: {found}")
    else:
        print("\n[-] Password not found in the wordlist.")

    print("\n***************** Thank you **********************\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
