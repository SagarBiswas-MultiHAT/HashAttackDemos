# Converter Script Guide

The scripts in this folder generate password hashes using modern algorithms. Each script can run interactively or accept CLI flags.

If you prefer a single unified entry point, use:

```bash
python -m hash_password_cracker --help
```

## Output file (JSON)

Every run appends a record to `hash_records.json` in the project root. Each record includes:

- `password` (plaintext, for learning only)
- `password_length`
- `algorithm`
- `hashing_algorithm` (same value as `algorithm`)
- `type` / `record_type`
- `hash`
- `params`
- `hash_format`
- `created_at`
- `source`

If you do **not** want plaintext stored, add `--redact`.

## Scripts

### `PassToArgon2id.py`

Hashes a password with Argon2id using secure defaults.

CLI options:
- `--password` Provide plaintext (otherwise prompt)
- `--time-cost`, `--memory-cost`, `--parallelism`, `--hash-len`, `--salt-len`
- `--output` JSON output path
- `--redact` Redact plaintext in JSON

Example:

```bash
python converters\PassToArgon2id.py --password "MySecret" --time-cost 3 --memory-cost 65536
```

### `PassToBcrypt.py`

Hashes a password with bcrypt.

CLI options:
- `--password` Provide plaintext (otherwise prompt)
- `--rounds` Cost factor (default 12)
- `--output` JSON output path
- `--redact` Redact plaintext in JSON

Example:

```bash
python converters\PassToBcrypt.py --password "MySecret" --rounds 12
```

### `PassToScrypt.py`

Hashes a password with scrypt.

CLI options:
- `--password` Provide plaintext (otherwise prompt)
- `--n`, `--r`, `--p`, `--dklen` Parameters
- `--salt-hex` Provide a salt (for reproducible demos)
- `--legacy-format` Output `<salt_hex>:<hash_hex>`
- `--output` JSON output path
- `--redact` Redact plaintext in JSON

Example:

```bash
python converters\PassToScrypt.py --password "MySecret" --n 16384 --r 8 --p 1
```

## Tips

- The JSON file is meant for learning and demos. Do **not** store plaintext passwords in real systems.
- For production, keep only the hash string and its parameters.
