# Library: `hash_password_cracker`

This folder contains the reusable core logic used by the scripts in `converters/` and `attackingScripts/`. You usually **import** these modules rather than running them directly.

## Unified CLI

You can also use the unified command-line interface:

```bash
python -m hash_password_cracker --help
```

This CLI wraps the converters and attack demos into one place. Running it without arguments prints a help summary. See `README.md` for full command examples.

## Modules

- `__init__.py`: Exposes the public API for imports.
- `__main__.py`: Implements the unified CLI entry point (`python -m hash_password_cracker`).
- `hashing.py`: Argon2id and bcrypt hashing + verification helpers.
- `scrypt_format.py`: Scrypt hashing and verification plus a portable storage format.
- `rainbow.py`: Rainbow table helpers for MD5 demo only.
- `wordlist.py`: Safe wordlist reader used by dictionary attacks.
- `attacks.py`: Shared dictionary attack logic.
- `records.py`: Writes hash records to a JSON file for reuse in demos.

## Example usage

```python
from hash_password_cracker import hash_bcrypt, verify_bcrypt

hashed = hash_bcrypt("myS3cret!", rounds=12)
print(verify_bcrypt("myS3cret!", hashed))
```

## Notes

- These helpers are designed for education and demos, not production systems.
- The `records.py` module can store plaintext passwords. Use `--redact` in the converter scripts to avoid that.
