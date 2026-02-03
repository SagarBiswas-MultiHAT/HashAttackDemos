from __future__ import annotations

from hash_password_cracker import dictionary_attack, hash_bcrypt


def test_dictionary_attack_finds_password(tmp_path):
    wordlist = tmp_path / "words.txt"
    wordlist.write_text("alpha\nbeta\ngamma\n", encoding="utf-8")

    target = "beta"
    hashed = hash_bcrypt(target, rounds=4)

    found = dictionary_attack(hashed, str(wordlist), "bcrypt")
    assert found == target


def test_dictionary_attack_not_found(tmp_path):
    wordlist = tmp_path / "words.txt"
    wordlist.write_text("alpha\nbeta\ngamma\n", encoding="utf-8")

    hashed = hash_bcrypt("delta", rounds=4)

    found = dictionary_attack(hashed, str(wordlist), "bcrypt")
    assert found is None
