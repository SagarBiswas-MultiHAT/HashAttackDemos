# Contributing Guide

Thanks for your interest in improving this project. This repository is intentionally simple and educational, so clarity matters more than cleverness.

## Quick start

1. Create a virtual environment and install dev dependencies:

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
```

2. Run tests and lint:

```bash
pytest
ruff check .
```

## Coding principles

- Prefer clear, readable code over clever optimizations.
- Keep the educational intent intact: explain why, not just how.
- Avoid changing defaults unless you also update docs and tests.

## Adding new features

If you add a new feature:

- Add tests in `tests/`
- Update `README.md` and any relevant script docs
- Keep CLI behavior backward compatible where possible

## Reporting issues

If you find a bug or unclear behavior, open an issue with:

- The script or function name
- The exact input used
- The observed output
- The expected output
