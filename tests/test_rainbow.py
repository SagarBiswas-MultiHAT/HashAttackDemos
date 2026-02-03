from __future__ import annotations

import hashlib

from hash_password_cracker import (
    build_rainbow_table,
    is_md5_hex,
    load_rainbow_table,
    lookup_md5_hash,
    lookup_plaintext,
)


def test_rainbow_build_and_lookup(tmp_path):
    wordlist = tmp_path / "words.txt"
    wordlist.write_text("alpha\nbeta\ngamma\n", encoding="utf-8")

    out_file = tmp_path / "rainbow.json"
    build_rainbow_table(str(wordlist), str(out_file))

    table = load_rainbow_table(str(out_file))
    md5_beta = hashlib.md5(b"beta").hexdigest()

    assert lookup_md5_hash(md5_beta, table) == "beta"

    found_hash, found_pw = lookup_plaintext("beta", table)
    assert found_hash == md5_beta
    assert found_pw == "beta"


def test_is_md5_hex():
    assert is_md5_hex("d41d8cd98f00b204e9800998ecf8427e")
    assert not is_md5_hex("not-a-hash")
    assert not is_md5_hex("abcd")
