"""Hash a password using bcrypt (interactive or CLI)."""

from __future__ import annotations

import argparse
import os
from getpass import getpass

from hash_password_cracker.hashing import hash_bcrypt
from hash_password_cracker.records import append_hash_record, build_hash_record

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Hash a password using bcrypt.")
    parser.add_argument(
        "--password",
        help="Password to hash (unsafe on shared shells). If omitted, prompts securely.",
    )
    parser.add_argument("--rounds", type=int, default=12, help="bcrypt cost factor.")
    parser.add_argument(
        "--output",
        default=os.path.join(PROJECT_ROOT, "hash_records.json"),
        help="JSON file to append hash records to.",
    )
    parser.add_argument(
        "--redact",
        action="store_true",
        help="Redact the plaintext password in the output JSON.",
    )
    return parser


def main() -> int:
    print("\n************** PASS -> BCRYPT ********************\n")

    parser = build_parser()
    args = parser.parse_args()

    password = args.password
    if password is None:
        password = getpass("Enter password to hash: ")

    hashed_password = hash_bcrypt(password, rounds=args.rounds)

    print("\n[+] Bcrypt Hash:")
    print(hashed_password)

    record = build_hash_record(
        password=password,
        algorithm="bcrypt",
        hashed=hashed_password,
        params={"rounds": args.rounds},
        source="converters/PassToBcrypt.py",
        hash_format="bcrypt-modular-crypt",
        include_plain=not args.redact,
    )
    output_path = os.path.abspath(args.output)
    append_hash_record(output_path, record)
    print(f"\n[+] Saved record to: {output_path}")

    print("\n***************** Thank you **********************\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
