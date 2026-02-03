"""Unified CLI for hash_password_cracker.

Usage:
  python -m hash_password_cracker --help
"""

from __future__ import annotations

import argparse
import os
import sys
from getpass import getpass

from hash_password_cracker import (
    DEFAULT_ARGON2_PARAMS,
    DEFAULT_SCRYPT_PARAMS,
    Argon2Params,
    ScryptParams,
    append_hash_record,
    build_hash_record,
    build_rainbow_table,
    dictionary_attack,
    hash_argon2id,
    hash_bcrypt,
    hash_scrypt,
    is_argon2_hash,
    is_bcrypt_hash,
    is_md5_hex,
    load_rainbow_table,
    lookup_md5_hash,
    lookup_plaintext,
)

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def resolve_path(path_value: str) -> str:
    return path_value if os.path.isabs(path_value) else os.path.join(PROJECT_ROOT, path_value)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Unified CLI for hashing utilities and attack demos."
    )
    subparsers = parser.add_subparsers(dest="group", required=True)

    hash_parser = subparsers.add_parser("hash", help="Generate password hashes")
    hash_sub = hash_parser.add_subparsers(dest="algorithm", required=True)

    argon_parser = hash_sub.add_parser("argon2id", help="Hash a password with Argon2id")
    argon_parser.add_argument("--password", help="Password to hash (unsafe on shared shells)")
    argon_parser.add_argument("--time-cost", type=int, default=DEFAULT_ARGON2_PARAMS.time_cost)
    argon_parser.add_argument("--memory-cost", type=int, default=DEFAULT_ARGON2_PARAMS.memory_cost)
    argon_parser.add_argument("--parallelism", type=int, default=DEFAULT_ARGON2_PARAMS.parallelism)
    argon_parser.add_argument("--hash-len", type=int, default=DEFAULT_ARGON2_PARAMS.hash_len)
    argon_parser.add_argument("--salt-len", type=int, default=DEFAULT_ARGON2_PARAMS.salt_len)
    argon_parser.add_argument(
        "--output",
        default=os.path.join(PROJECT_ROOT, "hash_records.json"),
        help="JSON file to append hash records to",
    )
    argon_parser.add_argument(
        "--redact",
        action="store_true",
        help="Redact plaintext password in JSON output",
    )

    bcrypt_parser = hash_sub.add_parser("bcrypt", help="Hash a password with bcrypt")
    bcrypt_parser.add_argument("--password", help="Password to hash (unsafe on shared shells)")
    bcrypt_parser.add_argument("--rounds", type=int, default=12)
    bcrypt_parser.add_argument(
        "--output",
        default=os.path.join(PROJECT_ROOT, "hash_records.json"),
        help="JSON file to append hash records to",
    )
    bcrypt_parser.add_argument(
        "--redact",
        action="store_true",
        help="Redact plaintext password in JSON output",
    )

    scrypt_parser = hash_sub.add_parser("scrypt", help="Hash a password with scrypt")
    scrypt_parser.add_argument("--password", help="Password to hash (unsafe on shared shells)")
    scrypt_parser.add_argument("--n", type=int, default=DEFAULT_SCRYPT_PARAMS.n)
    scrypt_parser.add_argument("--r", type=int, default=DEFAULT_SCRYPT_PARAMS.r)
    scrypt_parser.add_argument("--p", type=int, default=DEFAULT_SCRYPT_PARAMS.p)
    scrypt_parser.add_argument("--dklen", type=int, default=DEFAULT_SCRYPT_PARAMS.dklen)
    scrypt_parser.add_argument("--salt-hex", help="Provide hex salt for reproducible demos")
    scrypt_parser.add_argument(
        "--legacy-format",
        action="store_true",
        help="Output legacy format: <salt_hex>:<hash_hex>",
    )
    scrypt_parser.add_argument(
        "--output",
        default=os.path.join(PROJECT_ROOT, "hash_records.json"),
        help="JSON file to append hash records to",
    )
    scrypt_parser.add_argument(
        "--redact",
        action="store_true",
        help="Redact plaintext password in JSON output",
    )

    attack_parser = subparsers.add_parser("attack", help="Run attack demos")
    attack_sub = attack_parser.add_subparsers(dest="mode", required=True)

    dict_parser = attack_sub.add_parser(
        "dictionary", help="Dictionary verification attack"
    )
    dict_parser.add_argument("--hash", dest="stored_hash")
    dict_parser.add_argument("--wordlist")
    dict_parser.add_argument(
        "--algorithm",
        choices=["argon2id", "bcrypt", "scrypt"],
        help="Hash algorithm to verify against",
    )

    rainbow_parser = attack_sub.add_parser("rainbow", help="Rainbow table demo (MD5 only)")
    rainbow_sub = rainbow_parser.add_subparsers(dest="action", required=True)

    rainbow_build = rainbow_sub.add_parser("build", help="Build a rainbow table")
    rainbow_build.add_argument("--wordlist")
    rainbow_build.add_argument(
        "--out",
        default=os.path.join(PROJECT_ROOT, "rainbow_table.json"),
        help="Output JSON file",
    )

    rainbow_lookup = rainbow_sub.add_parser("lookup", help="Lookup a hash or plaintext")
    rainbow_lookup.add_argument("--input")
    rainbow_lookup.add_argument(
        "--table",
        default=os.path.join(PROJECT_ROOT, "rainbow_table.json"),
        help="Rainbow table JSON file",
    )

    hybrid_parser = attack_sub.add_parser("hybrid", help="Hybrid demo: MD5 rainbow + dictionary")
    hybrid_parser.add_argument("--hash", dest="stored_hash")
    hybrid_parser.add_argument("--wordlist")
    hybrid_parser.add_argument(
        "--algorithm",
        choices=["md5", "argon2id", "bcrypt", "scrypt"],
    )
    hybrid_parser.add_argument(
        "--rainbow",
        default=os.path.join(PROJECT_ROOT, "rainbow_table.json"),
        help="Rainbow table JSON file",
    )

    return parser


def run_hash(args: argparse.Namespace) -> int:
    if args.algorithm == "argon2id":
        password = args.password or getpass("Enter password to hash: ")
        params = Argon2Params(
            time_cost=args.time_cost,
            memory_cost=args.memory_cost,
            parallelism=args.parallelism,
            hash_len=args.hash_len,
            salt_len=args.salt_len,
        )
        hashed = hash_argon2id(password, params)
        record = build_hash_record(
            password=password,
            algorithm="argon2id",
            hashed=hashed,
            params={
                "time_cost": params.time_cost,
                "memory_cost": params.memory_cost,
                "parallelism": params.parallelism,
                "hash_len": params.hash_len,
                "salt_len": params.salt_len,
            },
            source="python -m hash_password_cracker hash argon2id",
            hash_format="phc-string",
            include_plain=not args.redact,
        )

    elif args.algorithm == "bcrypt":
        password = args.password or getpass("Enter password to hash: ")
        hashed = hash_bcrypt(password, rounds=args.rounds)
        record = build_hash_record(
            password=password,
            algorithm="bcrypt",
            hashed=hashed,
            params={"rounds": args.rounds},
            source="python -m hash_password_cracker hash bcrypt",
            hash_format="bcrypt-modular-crypt",
            include_plain=not args.redact,
        )

    elif args.algorithm == "scrypt":
        password = args.password or getpass("Enter password to hash: ")
        params = ScryptParams(n=args.n, r=args.r, p=args.p, dklen=args.dklen)
        salt = bytes.fromhex(args.salt_hex) if args.salt_hex else None
        hashed = hash_scrypt(
            password,
            params=params,
            salt=salt,
            include_params=not args.legacy_format,
        )
        hash_format = (
            "scrypt-legacy-salt-hash"
            if args.legacy_format
            else "scrypt$n=<N>,r=<r>,p=<p>$<salt>$<hash>"
        )
        record = build_hash_record(
            password=password,
            algorithm="scrypt",
            hashed=hashed,
            params={"n": params.n, "r": params.r, "p": params.p, "dklen": params.dklen},
            source="python -m hash_password_cracker hash scrypt",
            hash_format=hash_format,
            include_plain=not args.redact,
        )

    else:
        return 2

    output_path = os.path.abspath(args.output)
    append_hash_record(output_path, record)
    print("\n[+] Hash:")
    print(record["hash"])
    print(f"\n[+] Saved record to: {output_path}")
    return 0


def run_dictionary(args: argparse.Namespace) -> int:
    stored_hash = args.stored_hash or input("Enter the stored password hash: ").strip()
    prompt = "Choose algorithm (argon2id / bcrypt / scrypt): "
    algorithm = args.algorithm or input(prompt).strip().lower()
    wordlist = args.wordlist or input("Enter passwords file path: ").strip()

    if algorithm not in {"argon2id", "bcrypt", "scrypt"}:
        print(f"[!] Unsupported algorithm: {algorithm}")
        return 2

    if algorithm == "bcrypt" and not is_bcrypt_hash(stored_hash):
        print("[!] Invalid bcrypt hash format. Provide the full $2b$... string.")
        return 2
    if algorithm == "argon2id" and not is_argon2_hash(stored_hash):
        print("[!] Invalid Argon2id hash format.")
        print("Tip: in PowerShell, wrap hashes in single quotes to avoid $ expansion.")
        return 2

    try:
        found = dictionary_attack(stored_hash, resolve_path(wordlist), algorithm)
    except FileNotFoundError:
        print(f"[!] Wordlist not found: {resolve_path(wordlist)}")
        return 1

    if found:
        print(f"[+] Password found: {found}")
    else:
        print("[-] Password not found in the wordlist.")
    return 0


def run_rainbow(args: argparse.Namespace) -> int:
    if args.action == "build":
        wordlist = args.wordlist or input("Enter wordlist file path: ").strip()
        out_file = resolve_path(args.out)
        try:
            build_rainbow_table(resolve_path(wordlist), out_file)
        except FileNotFoundError:
            print(f"[!] Wordlist not found: {resolve_path(wordlist)}")
            return 1
        print(f"[+] Rainbow table built and saved to {out_file}")
        return 0

    if args.action == "lookup":
        user_input = args.input or input("Enter stolen MD5 hash OR plaintext password: ").strip()
        table_path = resolve_path(args.table)
        try:
            table = load_rainbow_table(table_path)
        except FileNotFoundError:
            print("[!] Rainbow table not found. Build it first.")
            return 1

        if is_md5_hex(user_input):
            result = lookup_md5_hash(user_input, table)
            if result:
                print(f"[+] Password cracked instantly: {result}")
            else:
                print("[-] Hash not found in rainbow table.")
            return 0

        found_hash, found_password = lookup_plaintext(user_input, table)
        if found_hash and found_password:
            print(f"[+] The plaintext you provided hashes to: {found_hash}")
            print(
                "[+] That hash maps to password in the rainbow table: "
                f"{found_password}"
            )
            if found_password != user_input:
                print(
                    "[i] Note: the table's stored password for that hash is "
                    f"different: {found_password}"
                )
            return 0

        print("[-] Plaintext not found in the rainbow table.")
        return 0

    return 2


def run_hybrid(args: argparse.Namespace) -> int:
    stored_hash = args.stored_hash or input("Enter the stored password hash: ").strip()
    prompt = "Choose algorithm (md5 / argon2id / bcrypt / scrypt): "
    algorithm = args.algorithm or input(prompt).strip().lower()

    if algorithm == "md5":
        table_path = resolve_path(args.rainbow)
        try:
            table = load_rainbow_table(table_path)
        except FileNotFoundError:
            print(f"[!] Rainbow table not found: {table_path}")
            return 1
        result = lookup_md5_hash(stored_hash, table)
        if result:
            print(f"[+] Password cracked instantly via rainbow table: {result}")
        else:
            print("[-] Hash not found in rainbow table.")
        return 0

    if algorithm not in {"argon2id", "bcrypt", "scrypt"}:
        print(f"[!] Unsupported algorithm: {algorithm}")
        return 2

    if algorithm == "bcrypt" and not is_bcrypt_hash(stored_hash):
        print("[!] Invalid bcrypt hash format. Provide the full $2b$... string.")
        return 2
    if algorithm == "argon2id" and not is_argon2_hash(stored_hash):
        print("[!] Invalid Argon2id hash format.")
        print("Tip: in PowerShell, wrap hashes in single quotes to avoid $ expansion.")
        return 2

    wordlist = args.wordlist
    if not wordlist:
        wordlist = input("Enter passwords file name (e.g. password.txt): ").strip()

    try:
        found = dictionary_attack(stored_hash, resolve_path(wordlist), algorithm)
    except FileNotFoundError:
        print(f"[!] Wordlist not found: {resolve_path(wordlist)}")
        return 1

    if found:
        print(f"[+] Password found: {found}")
    else:
        print("[-] Password not found in the wordlist.")
    return 0


def main() -> int:
    parser = build_parser()
    if len(sys.argv) == 1:
        parser.print_help()
        return 0
    args = parser.parse_args()

    if args.group == "hash":
        return run_hash(args)
    if args.group == "attack":
        if args.mode == "dictionary":
            return run_dictionary(args)
        if args.mode == "rainbow":
            return run_rainbow(args)
        if args.mode == "hybrid":
            return run_hybrid(args)

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
