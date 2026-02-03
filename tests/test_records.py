from __future__ import annotations

import json

from hash_password_cracker.records import append_hash_record, build_hash_record


def test_append_hash_record(tmp_path):
    path = tmp_path / "records.json"
    record = build_hash_record(
        password="secret",
        algorithm="bcrypt",
        hashed="$2b$12$abcdefghijklmnopqrstuvC3s9k7Mvtg2r5p1hZx1t0OrE9w2yG",
        params={"rounds": 12},
        source="tests",
        hash_format="bcrypt-modular-crypt",
        include_plain=False,
    )
    append_hash_record(str(path), record)

    data = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(data, list)
    assert data[0]["algorithm"] == "bcrypt"
    assert data[0]["password"] == "REDACTED"
