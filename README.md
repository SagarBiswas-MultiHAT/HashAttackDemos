# Password Hashing Utilities and Attack Demos

<div align="right">

[![CI](https://github.com/SagarBiswas-MultiHAT/HashAttackDemos/actions/workflows/python-ci.yml/badge.svg)](https://github.com/SagarBiswas-MultiHAT/HashAttackDemos/actions/workflows/python-ci.yml)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/github/license/SagarBiswas-MultiHAT/HashAttackDemos)](https://github.com/SagarBiswas-MultiHAT/HashAttackDemos/blob/main/LICENSE)
[![Tests](https://img.shields.io/badge/tests-pytest-brightgreen)](https://github.com/SagarBiswas-MultiHAT/HashAttackDemos/actions)
[![Last commit](https://img.shields.io/github/last-commit/SagarBiswas-MultiHAT/HashAttackDemos)](https://github.com/SagarBiswas-MultiHAT/HashAttackDemos)
[![Issues](https://img.shields.io/github/issues/SagarBiswas-MultiHAT/HashAttackDemos)](https://github.com/SagarBiswas-MultiHAT/HashAttackDemos/issues)

</div>

This repository is a compact, readable set of Python utilities that teach two things:

- How to hash passwords correctly with modern algorithms (Argon2id, bcrypt, scrypt)
- Why weak hashing (MD5) and rainbow tables are unsafe (educational demos)

The code is intentionally simple and heavily explained so a new developer or auditor can understand it end-to-end.

## Legal and ethical use

These scripts are for learning and defensive testing on data you own or are explicitly authorized to test. Do not use them against systems or datasets you do not own. If you are unsure, do not run the attack demos.

## Features at a glance

- Generate Argon2id, bcrypt, and scrypt hashes with sensible defaults
- Store every generated hash in a reusable JSON record file
- Verify hashes against a wordlist (dictionary attack)
- Build and query a rainbow table for MD5 (demo only)
- Hybrid flow showing a realistic attacker path (MD5 rainbow, then dictionary)
- A small reusable library (`hash_password_cracker`) with tests and CI
- Unified CLI: `python -m hash_password_cracker ...`

## Repository layout

- `hash_password_cracker/`: Reusable library code (hashing helpers, scrypt format, rainbow utilities)
- `converters/`: CLI/interactive scripts that hash passwords
- `attackingScripts/`: CLI/interactive attack demos (dictionary, rainbow, hybrid)
- `DeepDriveForLearners/`: Short, focused learning scripts
- `tests/`: Automated tests
- `.github/workflows/python-ci.yml`: GitHub Actions workflow (lint + tests)

## Requirements

- Python 3.8+ (tested with 3.11)
- Packages: `argon2-cffi`, `bcrypt`

`scrypt` is built into Python's `hashlib` module.

## Quickstart

1. Create and activate a virtual environment:

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
# macOS / Linux
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run any converter (interactive by default):

```bash
python converters\PassToArgon2id.py
python converters\PassToBcrypt.py
python converters\PassToScrypt.py
```

## Unified CLI (recommended)

The unified CLI wraps all converters and attack demos:

```bash
python -m hash_password_cracker --help
```

### PowerShell quoting tip (important)

Hash strings often include `$` characters. In PowerShell, `$` triggers variable expansion.

Use **single quotes** or escape `$` with a backtick:

```powershell
python -m hash_password_cracker attack dictionary --algorithm argon2id --hash '$argon2id$v=19$m=65536,t=3,p=4$...' --wordlist password.txt
python -m hash_password_cracker attack dictionary --algorithm bcrypt --hash '$2b$12$...' --wordlist password.txt
```

### Hash commands (examples)

```bash
python -m hash_password_cracker hash argon2id --password "MySecret"
python -m hash_password_cracker hash argon2id --password "MySecret" --memory-cost 65536 --time-cost 3
python -m hash_password_cracker hash bcrypt --password "MySecret" --rounds 12
python -m hash_password_cracker hash scrypt --password "MySecret" --n 16384 --r 8 --p 1
python -m hash_password_cracker hash scrypt --password "MySecret" --legacy-format
python -m hash_password_cracker hash bcrypt --password "MySecret" --output custom_records.json --redact
```

### Attack commands (examples)

```bash
python -m hash_password_cracker attack dictionary --algorithm bcrypt --hash '$2b$12$...' --wordlist password.txt
python -m hash_password_cracker attack dictionary --algorithm argon2id --hash '$argon2id$...' --wordlist password.txt
python -m hash_password_cracker attack rainbow build --wordlist password.txt
python -m hash_password_cracker attack rainbow lookup --input 5ebe2294ecd0e0f08eab7690d2a6ee69
python -m hash_password_cracker attack hybrid --algorithm md5 --hash 5ebe2294ecd0e0f08eab7690d2a6ee69
python -m hash_password_cracker attack hybrid --algorithm bcrypt --hash '$2b$12$...' --wordlist password.txt
```

### Full CLI reference

hash argon2id
- `--password` Plaintext to hash (if omitted, you are prompted securely)
- `--time-cost` Iterations (CPU cost)
- `--memory-cost` Memory in KiB (Argon2 uses this to resist GPUs)
- `--parallelism` Parallel lanes
- `--hash-len` Output length in bytes
- `--salt-len` Salt length in bytes
- `--output` JSON output path
- `--redact` Redact plaintext in JSON

hash bcrypt
- `--password` Plaintext to hash (if omitted, you are prompted securely)
- `--rounds` Cost factor (2^rounds)
- `--output` JSON output path
- `--redact` Redact plaintext in JSON

hash scrypt
- `--password` Plaintext to hash (if omitted, you are prompted securely)
- `--n`, `--r`, `--p`, `--dklen` Scrypt parameters
- `--salt-hex` Provide a hex salt for reproducible demos
- `--legacy-format` Output `<salt_hex>:<hash_hex>`
- `--output` JSON output path
- `--redact` Redact plaintext in JSON

attack dictionary
- `--algorithm` `argon2id`, `bcrypt`, `scrypt`
- `--hash` Stored hash string
- `--wordlist` Path to wordlist

attack rainbow build
- `--wordlist` Wordlist file used to build the table
- `--out` Output JSON file

attack rainbow lookup
- `--input` MD5 hash or plaintext
- `--table` Rainbow JSON file

attack hybrid
- `--algorithm` `md5`, `argon2id`, `bcrypt`, `scrypt`
- `--hash` Stored hash string
- `--wordlist` Path to wordlist (required for non-MD5)
- `--rainbow` Rainbow JSON file

## Hash record output (JSON)

Every converter appends a record to `hash_records.json` in the project root. Each record contains:

- `password` (plaintext, for learning only)
- `password_length`
- `type` / `record_type`
- `algorithm`
- `hashing_algorithm` (same value as `algorithm`)
- `hash`
- `params`
- `hash_format`
- `created_at`
- `source`

If you do **not** want plaintext stored, add `--redact`.

## Library usage (importable API)

You can import and reuse the library directly:

```python
from hash_password_cracker import (
    Argon2Params,
    hash_argon2id,
    verify_argon2id,
    hash_bcrypt,
    verify_bcrypt,
    hash_scrypt,
    verify_scrypt,
)

# Argon2id
argon_hash = hash_argon2id("myS3cret!", Argon2Params(time_cost=3, memory_cost=65536))
assert verify_argon2id("myS3cret!", argon_hash)

# bcrypt
bcrypt_hash = hash_bcrypt("myS3cret!", rounds=12)
assert verify_bcrypt("myS3cret!", bcrypt_hash)

# scrypt
scrypt_hash = hash_scrypt("myS3cret!")
assert verify_scrypt("myS3cret!", scrypt_hash)
```

## Hash formats and verification

- Argon2id and bcrypt output strings that already include parameters and salt. Store them as-is.
- Scrypt outputs a portable format by default:

```
n=<N>,r=<r>,p=<p>$<salt_hex>$<hash_hex>
```

Legacy format is still supported (for old demos):

```
<salt_hex>:<hash_hex>
```

Verification always means: re-run the same algorithm with the same parameters and salt, then compare the derived key.

## Parameter guidance (starting points)

These defaults are reasonable for a demo and can be tuned higher for production based on your hardware and latency targets:

- Argon2id: `time_cost=3`, `memory_cost=65536`, `parallelism=4`
- bcrypt: `rounds=12`
- scrypt: `n=16384`, `r=8`, `p=1`

## Testing and linting

Run tests and lint locally:

```bash
pip install -r requirements-dev.txt
pytest
ruff check .
```

CI runs the same checks in `.github/workflows/python-ci.yml`.

## Documentation map

For deeper usage guides, see:

- `converters/readme.md`
- `attackingScripts/readme.md`
- `hash_password_cracker/readme.md`
- `DeepDriveForLearners/readme.md`

## Limitations and safety notes

- These scripts are not production authentication systems. They are educational utilities.
- The rainbow table demo is intentionally unrealistic for modern systems; it exists to show why MD5 is broken.
- Do not use the attack demos on real systems or data without explicit permission.

## Suggested next steps (optional)

If you want to extend this project:

- Add a small CLI wrapper that bundles all commands under one entry point
- Expand tests to cover error cases and edge inputs
- Package and publish the library for easier reuse
