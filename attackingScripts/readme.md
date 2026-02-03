# Attack Script Guide

This folder contains educational attack demonstrations. They are intentionally simple and are meant for defensive learning only.

If you prefer a single unified entry point, use:

```bash
python -m hash_password_cracker --help
```

## PowerShell quoting tip

Hashes contain `$` characters. In PowerShell, wrap hash strings in **single quotes** to avoid variable expansion:

```powershell
python attackingScripts\dictionaryAttack.py --algorithm bcrypt --hash '$2b$12$...' --wordlist password.txt
```

## What each script does

- `dictionaryAttack.py`: Verifies a stored hash against a wordlist by hashing each word and checking for a match. This works even for salted hashes because verification reuses the original hash parameters.
- `rainbowAttack.py`: Builds and queries a rainbow table for MD5 only. This demonstrates why _fast, unsalted_ hashes are dangerous.
- `hybridAttack.py`: Demonstrates a two-phase workflow by using a rainbow lookup for MD5, then falling back to dictionary verification for Argon2id, bcrypt, or scrypt.

## Dictionary vs Rainbow vs Hybrid

Dictionary attack:

- Slow but general
- Works against modern, salted hashes because it verifies using the original parameters

Rainbow table:

- Very fast lookup
- Only works for _unsalted_ fast hashes like MD5
- Precomputation cost is high, so it is unrealistic for modern algorithms

Hybrid attack:

- Best of both worlds in a demo
- Uses rainbow lookup when it can, and dictionary verification otherwise

## CLI reference

`dictionaryAttack.py` options:

- `--algorithm` One of `argon2id`, `bcrypt`, `scrypt`
- `--hash` Stored hash string (must be the _full_ hash, not a placeholder)
- `--wordlist` Path to a wordlist file

`rainbowAttack.py build` options:

- `--wordlist` Wordlist file to build the table from
- `--out` Output JSON file (default: `rainbow_table.json` in project root)

`rainbowAttack.py lookup` options:

- `--input` MD5 hash or plaintext password
- `--table` Path to JSON rainbow table

`hybridAttack.py` options:

- `--algorithm` One of `md5`, `argon2id`, `bcrypt`, `scrypt`
- `--hash` Stored hash string
- `--wordlist` Wordlist path (required for non-MD5 algorithms)
- `--rainbow` Path to the MD5 rainbow table JSON

## Unified CLI equivalents

```bash
python -m hash_password_cracker attack dictionary --algorithm bcrypt --hash '$2b$12$...' --wordlist password.txt
python -m hash_password_cracker attack rainbow build --wordlist password.txt
python -m hash_password_cracker attack rainbow lookup --input 5ebe2294ecd0e0f08eab7690d2a6ee69
python -m hash_password_cracker attack hybrid --algorithm md5 --hash 5ebe2294ecd0e0f08eab7690d2a6ee69
```

## Examples

Dictionary attack (bcrypt):

```bash
python attackingScripts\dictionaryAttack.py --algorithm bcrypt --hash '$2b$12$szA0tYubi/ij4vE9pQ4OjeJSw04fVXelDgiDm.O6/XijW92xiWlXC' --wordlist password.txt
```

Rainbow table build + lookup:

```bash
python attackingScripts\rainbowAttack.py build --wordlist password.txt
python attackingScripts\rainbowAttack.py lookup --input 5ebe2294ecd0e0f08eab7690d2a6ee69
```

Hybrid attack (MD5):

```bash
python attackingScripts\hybridAttack.py --algorithm md5 --hash 5ebe2294ecd0e0f08eab7690d2a6ee69
```

Hybrid attack (bcrypt):

```bash
python attackingScripts\hybridAttack.py --algorithm bcrypt --hash '$2b$12$szA0tYubi/ij4vE9pQ4OjeJSw04fVXelDgiDm.O6/XijW92xiWlXC' --wordlist password.txt
```

## Safety note

Only use these scripts on data you own or are explicitly authorized to test.
