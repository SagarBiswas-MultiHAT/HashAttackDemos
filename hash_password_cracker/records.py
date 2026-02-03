"""Create and persist hash records for later reuse."""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from typing import Any


def build_hash_record(
    password: str,
    algorithm: str,
    hashed: str,
    params: dict[str, Any] | None = None,
    source: str | None = None,
    hash_format: str | None = None,
    include_plain: bool = True,
) -> dict[str, Any]:
    """Build a normalized hash record dictionary."""
    record: dict[str, Any] = {
        "record_version": 1,
        "record_type": "password_hash",
        "type": "password_hash",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "algorithm": algorithm,
        "hashing_algorithm": algorithm,
        "hash": hashed,
        "params": params or {},
        "hash_format": hash_format or "",
        "password_length": len(password),
        "source": source or "",
    }

    record["password"] = password if include_plain else "REDACTED"

    return record


def append_hash_record(path: str, record: dict[str, Any]) -> list[dict[str, Any]]:
    """Append a record to a JSON list on disk (creating if needed)."""
    records: list[dict[str, Any]] = []

    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)

    if os.path.exists(path):
        with open(path, encoding="utf-8") as handle:
            try:
                existing = json.load(handle)
            except json.JSONDecodeError:
                existing = []

        if isinstance(existing, list):
            records = existing
        elif isinstance(existing, dict):
            records = [existing]
        else:
            raise ValueError("Existing record file must be a list or object.")

    records.append(record)

    with open(path, "w", encoding="utf-8") as handle:
        json.dump(records, handle, indent=2, ensure_ascii=False)

    return records
