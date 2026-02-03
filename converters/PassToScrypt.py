"""Hash a password using scrypt (interactive or CLI)."""

from __future__ import annotations

import argparse
import os
from getpass import getpass

from hash_password_cracker.records import append_hash_record, build_hash_record
from hash_password_cracker.scrypt_format import DEFAULT_SCRYPT_PARAMS, ScryptParams, hash_scrypt

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Hash a password using scrypt.")
    parser.add_argument(
        "--password",
        help="Password to hash (unsafe on shared shells). If omitted, prompts securely.",
    )
    parser.add_argument("--n", type=int, default=DEFAULT_SCRYPT_PARAMS.n)
    parser.add_argument("--r", type=int, default=DEFAULT_SCRYPT_PARAMS.r)
    parser.add_argument("--p", type=int, default=DEFAULT_SCRYPT_PARAMS.p)
    parser.add_argument("--dklen", type=int, default=DEFAULT_SCRYPT_PARAMS.dklen)
    parser.add_argument(
        "--salt-hex",
        help="Optional hex salt for reproducible output (unsafe for real passwords).",
    )
    parser.add_argument(
        "--legacy-format",
        action="store_true",
        help="Output legacy format: <salt_hex>:<hash_hex>.",
    )
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
    print("\n************** PASS -> SCRYPT ********************\n")

    parser = build_parser()
    args = parser.parse_args()

    password = args.password
    if password is None:
        password = getpass("Enter password to hash: ")

    params = ScryptParams(n=args.n, r=args.r, p=args.p, dklen=args.dklen)
    salt = bytes.fromhex(args.salt_hex) if args.salt_hex else None

    hashed_password = hash_scrypt(
        password,
        params=params,
        salt=salt,
        include_params=not args.legacy_format,
    )

    print("\n[+] Scrypt Hash:")
    print(hashed_password)

    hash_format = (
        "scrypt-legacy-salt-hash"
        if args.legacy_format
        else "scrypt$n=<N>,r=<r>,p=<p>$<salt>$<hash>"
    )
    record = build_hash_record(
        password=password,
        algorithm="scrypt",
        hashed=hashed_password,
        params={
            "n": params.n,
            "r": params.r,
            "p": params.p,
            "dklen": params.dklen,
        },
        source="converters/PassToScrypt.py",
        hash_format=hash_format,
        include_plain=not args.redact,
    )
    output_path = os.path.abspath(args.output)
    append_hash_record(output_path, record)
    print(f"\n[+] Saved record to: {output_path}")

    print("\n***************** Thank you **********************\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
