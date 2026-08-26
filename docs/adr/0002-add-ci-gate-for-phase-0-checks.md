# 0002 — Add CI gate for Phase 0 checks

**Status:** Accepted

## Context

`scripts/verify_setup.py` and `tests/test_pipeline_validator.py` already serve as this repo's
Phase 0 quality gate — `README.md` explicitly says "If `verify_setup.py` exits non-zero, stop."
But both only run when someone manually types the command in a terminal. Nothing in the repo
itself proves to a reader (instructor, reviewer, or future me) that these gates currently pass,
short of trusting `PROGRESS.md`'s handwritten log.

## Decision

Add a GitHub Actions workflow (`.github/workflows/ci.yml`) that runs on every push and pull
request to `main`:
1. Install dependencies from `requirements.txt`
2. Run `python scripts/verify_setup.py`
3. Run `pytest tests/ -v`

## Consequences

- Pass/fail is now visible directly on the repo as a commit status check, without requiring
  anyone to run anything locally.
- This automates an existing manual gate — it does not introduce a new methodology or change
  local development workflow.
- Pinned to Python 3.12 in CI (a stable, widely available runner version) even though local
  `.venv` runs 3.14; nothing in `requirements.txt` requires a specific minor version.
