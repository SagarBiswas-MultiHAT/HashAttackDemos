#!/usr/bin/env python3
"""
Rainbow table demo (MD5 only).

Modes:
- build: create rainbow_table.json from a wordlist
- lookup: lookup an MD5 hash or plaintext password in the table
"""

from __future__ import annotations

# Enables postponed evaluation of type hints
# This allows using types that are not yet defined (e.g., self-referencing classes)
# Useful for compatibility with older Python versions (before Python 3.11)
# Delays evaluation of type hints so classes can reference themselves
# Helps avoid errors in older Python versions
import argparse
import os

from hash_password_cracker import (
    build_rainbow_table,
    is_md5_hex,
    load_rainbow_table,
    lookup_md5_hash,
    lookup_plaintext,
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
    parser = argparse.ArgumentParser(description="Rainbow table demo (MD5 only).")
    subparsers = parser.add_subparsers(dest="command")

    build_parser = subparsers.add_parser("build", help="Build a rainbow table")
    build_parser.add_argument("--wordlist", required=False, help="Path to wordlist file.")
    build_parser.add_argument("--out", default=RAINBOW_FILE, help="Output JSON file.")

    lookup_parser = subparsers.add_parser("lookup", help="Lookup a hash or plaintext")
    lookup_parser.add_argument("--input", dest="user_input", help="MD5 hash or plaintext.")
    lookup_parser.add_argument("--table", default=RAINBOW_FILE, help="Rainbow table JSON file.")

    return parser


def run_build(wordlist_path: str, out_file: str) -> int:
    try:
        build_rainbow_table(wordlist_path, out_file)
    except FileNotFoundError:
        print(f"[!] Wordlist not found: {wordlist_path}")
        return 1

    print(f"[+] Rainbow table built and saved to {out_file}")
    return 0


def run_lookup(user_input: str, table_path: str) -> int:
    try:
        table = load_rainbow_table(table_path)
    except FileNotFoundError:
        print("[!] Rainbow table not found. Build it first (use 'build').")
        return 1

    candidate = user_input.strip()

    if is_md5_hex(candidate):
        result = lookup_md5_hash(candidate, table)
        if result:
            print(f"[+] Password cracked instantly: {result}")
        else:
            print("[-] Hash not found in rainbow table.")
        return 0

    found_hash, found_password = lookup_plaintext(candidate, table)
    if found_hash and found_password:
        print(f"[+] The plaintext you provided hashes to: {found_hash}")
        print(
            "[+] That hash maps to password in the rainbow table: "
            f"{found_password}"
        )
        if found_password != candidate:
            print(
                "[i] Note: the table's stored password for that hash is "
                f"different: {found_password}"
            )
        return 0

    print("[-] Plaintext not found in the rainbow table.")
    return 0


def main() -> int:
    print("\n************** RAINBOW TABLE DEMO ******************\n")

    parser = build_parser()
    args = parser.parse_args()

    if args.command == "build":
        wordlist_path = args.wordlist or input("Enter wordlist file path: ").strip()
        out_file = resolve_path(args.out)
        return run_build(resolve_path(wordlist_path), out_file)

    if args.command == "lookup":
        prompt = "Enter stolen MD5 hash OR plaintext password: "
        user_input = args.user_input or input(prompt).strip()
        table_path = resolve_path(args.table)
        return run_lookup(user_input, table_path)

    choice = input("Build table or lookup? (build/lookup): ").strip().lower()
    if choice == "build":
        wordlist_path = input("Enter wordlist file path: ").strip()
        out_file = resolve_path(RAINBOW_FILE)
        return run_build(resolve_path(wordlist_path), out_file)
    if choice == "lookup":
        user_input = input("Enter stolen MD5 hash OR plaintext password: ").strip()
        table_path = resolve_path(RAINBOW_FILE)
        return run_lookup(user_input, table_path)

    print("[!] Invalid choice. Use 'build' or 'lookup'.")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
