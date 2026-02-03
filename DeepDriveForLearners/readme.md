# DeepDriveForLearners

This folder contains small, focused learning scripts. Each file is short on purpose so you can read it in a few minutes and understand the concept.

## Scripts

- `DictionaryToBuildaRainbowTable.py`: Builds a tiny rainbow table from a small dictionary and cracks a simulated MD5 hash.
- `WhyRainbowTablesFailwithArgon2id.py`: Shows that the same password produces different Argon2id hashes because of random salt.
- `SaltedVsUnsaltedDemo.py`: Demonstrates how salting changes hashes even when the password is the same.

## How to run

From the project root:

```bash
python DeepDriveForLearners\DictionaryToBuildaRainbowTable.py
python DeepDriveForLearners\WhyRainbowTablesFailwithArgon2id.py
python DeepDriveForLearners\SaltedVsUnsaltedDemo.py
```

## Learning goal

These are conceptual demos, not production patterns. They exist to help you internalize why modern password hashing uses salt and cost factors.
