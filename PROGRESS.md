# L02 Progress Log

**Governing sentence:** Test before code. Spec before implementation. Human checkpoint before every advance.

## Current state
- **Phase:** 0 (Setup) — complete
- **Last completed unit:** C — Cell 5 (DataFrame)
- **Next unit:** D — next notebook cell
- **Environment:** .venv created | verify_setup: PASS | pytest: PASS (18 passed)

## Unit log
| # | Unit | Assertion | Code | Validated | Commit | Notes |
|---|------|-----------|------|-----------|--------|-------|
| 0 | Phase 0 setup | n/a | n/a | PASS | — | .venv created, requirements installed, verify_setup.py PASS, pytest 18/18 PASS |
| A | Cell 2 — Imports | No exception; prints success banner + pandas/numpy versions matching Phase 0 | Pre-written (untouched) | PASS | 5944e4e | Required adding scikit-learn (not in original requirements.txt) — see docs/adr/0001-add-scikit-learn-for-lab-notebook.md. Output: pandas 3.0.5, numpy 2.5.2, no errors |
| B | Cell 4 — load_iris | No exception; shape (150, 4); 4 feature names; 3 target classes | Pre-written (untouched) | PASS | 49f4dde | Ran in same kernel session as Cell 2. Output: shape (150, 4), features = 4 sepal/petal measurements, target classes = setosa/versicolor/virginica |
| C | Cell 5 — DataFrame | No exception; head shows 5 columns (4 measurements + species=setosa); info shows 150 entries, 5 columns, no nulls | Pre-written (untouched) | PASS | pending | Ran in same kernel session as Cells 2 and 4. Trailing `None` after df.info() confirmed as expected notebook noise |

## Session handoffs
### 2026-08-22
- Done: repo structure clean and pushed; system operating files local; template v1.1 locked; Phase 0 gates run — verify_setup.py PASS, pytest 18/18 PASS; Unit A (Cell 2 — Imports) PASS after adding scikit-learn dependency (ADR 0001); Unit B (Cell 4 — load_iris) PASS; Unit C (Cell 5 — DataFrame) PASS
- Blocked: none
- Next exact action: begin Unit D — next notebook cell (Builder Loop: C1 → assertion first → run → C2 commit)
