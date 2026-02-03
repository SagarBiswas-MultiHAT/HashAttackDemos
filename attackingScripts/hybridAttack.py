"""Hybrid attack demo: MD5 rainbow lookup, then dictionary verification."""

from __future__ import annotations

import argparse
import os

from hash_password_cracker import (
    SUPPORTED_ALGORITHMS,
    dictionary_attack,
    is_argon2_hash,
    is_bcrypt_hash,
    load_rainbow_table,
    lookup_md5_hash,
)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

RAINBOW_FILE = os.path.join(PROJECT_ROOT, "rainbow_table.json")


def resolve_path(user_input_path: str) -> str:
    return (
        user_input_path
        if os.path.isabs(user_input_path)
        else os.path.join(PROJECT_ROOT, user_input_path)
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Hybrid password attack demo.")
    parser.add_argument("--hash", dest="stored_hash", help="Stored hash to verify.")
    parser.add_argument("--wordlist", help="Path to wordlist file.")
    parser.add_argument(
        "--algorithm",
        choices=sorted(list(SUPPORTED_ALGORITHMS.keys()) + ["md5"]),
        help="Hash algorithm to verify against.",
    )
    parser.add_argument(
        "--rainbow",
        default=RAINBOW_FILE,
        help="Path to rainbow table JSON (MD5 only).",
    )
    return parser


def main() -> int:
    print("\n************** HYBRID PASSWORD ATTACK ******************\n")

    parser = build_parser()
    args = parser.parse_args()

    stored_hash = args.stored_hash or input("Enter the stored password hash: ").strip()
    algorithm = (
        args.algorithm
        or input("Choose algorithm (md5 / argon2id / bcrypt / scrypt): ").strip().lower()
    )

    wordlist_name = args.wordlist
    if algorithm != "md5" and not wordlist_name:
        wordlist_name = input("Enter passwords file name (e.g. password.txt): ").strip()

    if algorithm == "md5":
        print("[*] Phase 1: Rainbow table lookup...")
        rainbow_path = resolve_path(args.rainbow)
        try:
            table = load_rainbow_table(rainbow_path)
        except FileNotFoundError:
            print(f"[!] Rainbow table not found: {rainbow_path}")
            return 1

        result = lookup_md5_hash(stored_hash, table)
        if result:
            print(f"[+] Password cracked instantly via rainbow table: {result}")
        else:
            print("[-] Hash not found in rainbow table.")
        print("\n***************** Done **********************\n")
        return 0

    if algorithm not in SUPPORTED_ALGORITHMS:
        print(f"\n[!] Unsupported algorithm: {algorithm}")
        print("Supported: md5, argon2id, bcrypt, scrypt")
        return 2

    if algorithm == "bcrypt" and not is_bcrypt_hash(stored_hash):
        print("\n[!] Invalid bcrypt hash format.")
        print("Tip: provide the full $2b$... hash string, not a placeholder.")
        return 2

    if algorithm == "argon2id" and not is_argon2_hash(stored_hash):
        print("\n[!] Invalid Argon2id hash format.")
        print("Tip: in PowerShell, wrap hashes in single quotes to avoid $ expansion.")
        return 2

    print("[*] Phase 2: Dictionary attack (verification-based)...")
    wordlist_path = resolve_path(wordlist_name)

    try:
        found = dictionary_attack(stored_hash, wordlist_path, algorithm)
    except FileNotFoundError:
        print(f"\n[!] Error: Wordlist not found -> {wordlist_path}")
        return 1

    if found:
        print(f"\n[+] Password found: {found}")
    else:
        print("\n[-] Password not found in the wordlist.")

    print("\n***************** Thank you **********************\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
