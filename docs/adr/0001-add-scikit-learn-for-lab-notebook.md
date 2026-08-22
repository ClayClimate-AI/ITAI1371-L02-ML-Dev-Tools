# 0001 — Add scikit-learn for lab notebook

**Status:** Accepted

## Context

`Tech_Spec.md` / `requirements.txt` originally excluded scikit-learn (along with seaborn,
plotly, torch, tensorflow), on the basis that Module 2's core stack is pandas + NumPy +
matplotlib. Phase 0 environment verification (`scripts/verify_setup.py`) passed cleanly under
that assumption.

However, the assignment's own notebook (`src/Module_02_Lab_Exercise.ipynb`) is pre-written and
not authored by this repo — Cell 2 (Imports) contains `from sklearn import datasets`, and later
cells load the Iris dataset via `sklearn.datasets.load_iris`. Running the notebook as given
requires scikit-learn regardless of what the original Tech_Spec assumed. Attempting Cell 2
against the Phase-0 environment raised `ModuleNotFoundError: No module named 'sklearn'`,
confirming the gap before any code was changed.

## Decision

Treat the notebook as the source of truth for its own dependencies. Add `scikit-learn>=1.4` to
`requirements.txt` as a lab dependency, install it into `.venv`, and leave the pre-written
notebook cell untouched.

## Consequences

- The local environment now matches what the official notebook actually imports; Cell 2 can run
  without modification.
- Phase 0's `verify_setup.py` did not check for scikit-learn and should be revisited if future
  units depend on functional checks beyond import success.
- `requirements.txt`'s "Explicitly NOT included" list is amended to drop scikit-learn; seaborn,
  plotly, torch, and tensorflow remain excluded until a similar need arises.
