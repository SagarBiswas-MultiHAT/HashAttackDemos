"""Hash a password using Argon2id (interactive or CLI)."""

from __future__ import annotations

import argparse
import os
from getpass import getpass

from hash_password_cracker.hashing import DEFAULT_ARGON2_PARAMS, Argon2Params, hash_argon2id
from hash_password_cracker.records import append_hash_record, build_hash_record

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Hash a password using Argon2id.")
    parser.add_argument(
        "--password",
        help="Password to hash (unsafe on shared shells). If omitted, prompts securely.",
    )
    parser.add_argument("--time-cost", type=int, default=DEFAULT_ARGON2_PARAMS.time_cost)
    parser.add_argument("--memory-cost", type=int, default=DEFAULT_ARGON2_PARAMS.memory_cost)
    parser.add_argument("--parallelism", type=int, default=DEFAULT_ARGON2_PARAMS.parallelism)
    parser.add_argument("--hash-len", type=int, default=DEFAULT_ARGON2_PARAMS.hash_len)
    parser.add_argument("--salt-len", type=int, default=DEFAULT_ARGON2_PARAMS.salt_len)
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
    print("\n************** PASS -> ARGON2id ******************\n")

    parser = build_parser()
    args = parser.parse_args()

    password = args.password
    if password is None:
        password = getpass("Enter password to hash: ")

    params = Argon2Params(
        time_cost=args.time_cost,
        memory_cost=args.memory_cost,
        parallelism=args.parallelism,
        hash_len=args.hash_len,
        salt_len=args.salt_len,
    )

    hashed_password = hash_argon2id(password, params)

    print("\n[+] Argon2id Hash:")
    print(hashed_password)

    record = build_hash_record(
        password=password,
        algorithm="argon2id",
        hashed=hashed_password,
        params={
            "time_cost": params.time_cost,
            "memory_cost": params.memory_cost,
            "parallelism": params.parallelism,
            "hash_len": params.hash_len,
            "salt_len": params.salt_len,
        },
        source="converters/PassToArgon2id.py",
        hash_format="phc-string",
        include_plain=not args.redact,
    )
    output_path = os.path.abspath(args.output)
    append_hash_record(output_path, record)
    print(f"\n[+] Saved record to: {output_path}")

    print("\n***************** Thank you **********************\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
