# L02 Progress Log

**Governing sentence:** Test before code. Spec before implementation. Human checkpoint before every advance.

## Current state
- **Phase:** 0 (Setup) — complete
- **Last completed unit:** H — Cell 14 (markdown reflection, filled in)
- **Next unit:** Harvest — not started (awaiting go-ahead)
- **Environment:** .venv created | verify_setup: PASS | pytest: PASS (18 passed) | CI: PASS (run #1, ad12277)

## Unit log
| # | Unit | Assertion | Code | Validated | Commit | Notes |
|---|------|-----------|------|-----------|--------|-------|
| 0 | Phase 0 setup | n/a | n/a | PASS | — | .venv created, requirements installed, verify_setup.py PASS, pytest 18/18 PASS |
| A | Cell 2 — Imports | No exception; prints success banner + pandas/numpy versions matching Phase 0 | Pre-written (untouched) | PASS | 5944e4e | Required adding scikit-learn (not in original requirements.txt) — see docs/adr/0001-add-scikit-learn-for-lab-notebook.md. Output: pandas 3.0.5, numpy 2.5.2, no errors |
| B | Cell 4 — load_iris | No exception; shape (150, 4); 4 feature names; 3 target classes | Pre-written (untouched) | PASS | 49f4dde | Ran in same kernel session as Cell 2. Output: shape (150, 4), features = 4 sepal/petal measurements, target classes = setosa/versicolor/virginica |
| C | Cell 5 — DataFrame | No exception; head shows 5 columns (4 measurements + species=setosa); info shows 150 entries, 5 columns, no nulls | Pre-written (untouched) | PASS | 72c1533 | Ran in same kernel session as Cells 2 and 4. Trailing `None` after df.info() confirmed as expected notebook noise |
| D | Cell 7 — Scatter plot | No exception; 3 colored clusters (red/blue/green); correct axis labels, title, legend; congratulations line printed | Pre-written (untouched) | PASS | 7057c8d | Ran in same kernel session as Cells 2, 4, 5. Confirmed visually: red=setosa, blue=versicolor, green=virginica clusters distinct |
| E | Cell 9 — groupby stats | No exception; grouped means by species match known Iris values; value_counts shows 50/50/50 | Pre-written (untouched) | PASS | 7562003 | Ran in same kernel session with df from Cell 5. Confirmed printed means and 50/50/50 species counts |
| F | Cell 12 — Task 1 (mean/std + asserts) | No exception, including no AssertionError; prints mean 5.84 cm, std 0.83 cm; ✅ Task 1 line printed | Pre-written (untouched) | PASS | 6bbf1d9 | Notebook's own inline assert checks (isinstance on np.floating) passed silently. Ran in same kernel session with df, np from Cells 5/2 |
| G | Cell 13 — Task 2 (bar chart) | No exception; 3 equal-height bars (50 each); correct title/axis labels; distribution dict shows 50/50/50; ✅ Task 2 line printed | Pre-written (untouched) | PASS | 89eb363 | Ran in same kernel session with plt, df from Cells 2/5. Confirmed visually: 3 bars height 50 for setosa/versicolor/virginica |
| H | Cell 14 — Markdown reflection | FILL-IN placeholders replaced with real content; no code cells touched; content matches human-approved draft exactly | Human-authored (via C1-approved draft) | PASS | pending | Dataset Overview, Key Findings, Questions, Reflection sections written per approved draft; confirmed by human review of rendered cell |

## Session handoffs
### 2026-08-25
- Done: repo structure clean and pushed; system operating files local; template v1.1 locked; Phase 0 gates run — verify_setup.py PASS, pytest 18/18 PASS; CI workflow added and passing (ADR 0002); Unit A (Cell 2 — Imports) PASS after adding scikit-learn dependency (ADR 0001); Unit B (Cell 4 — load_iris) PASS; Unit C (Cell 5 — DataFrame) PASS; Unit D (Cell 7 — scatter plot) PASS; Unit E (Cell 9 — groupby stats) PASS; Unit F (Cell 12 — Task 1) PASS; Unit G (Cell 13 — Task 2) PASS; Unit H (Cell 14 — markdown reflection) PASS
- Blocked: none
- Next exact action: Harvest — export notebook to PDF, write reflective journal deliverable, prepare final submission (not started; awaiting go-ahead)
