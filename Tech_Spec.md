# Tech_Spec.md

> **Phase 1 — PLAN.** This document owns the *how*. It defines boundaries the implementation may not cross. When `Product_Spec.md` and this file disagree, the product spec wins and this file is amended.

---

## 1. Stack

| Layer | Choice | Version constraint |
|---|---|---|
| Language | Python | 3.10+ (3.8 minimum; see note below) |
| Environment | `venv` at `.venv/` in repo root | stdlib only |
| DataFrames | pandas | `>=2.0` |
| Arrays | NumPy | `>=1.24` |
| Plotting | matplotlib | `>=3.7` |
| Notebook kernel | ipykernel | `>=6.0` |
| Testing | pytest | `>=7.0` |

> **Python version note:** `src/pipeline_validator.py` uses `from __future__ import annotations` so that `X | Y` union type hints work on 3.8/3.9. Without that import the module raises `TypeError` at import time on those versions. If you strip the import, you have raised the floor to 3.10 — update this table.

**Forbidden without a spec amendment:** scikit-learn, seaborn, plotly, TensorFlow, PyTorch, any cloud SDK, any HTTP client.

---

## 2. The 9 Pillars — Boundaries

| Pillar | Boundary instruction |
|---|---|
| **UI** | Jupyter notebook cells only. No widgets, no `ipywidgets`, no interactive callbacks — none of it survives PDF export. |
| **Routing** | N/A. Single linear notebook, top to bottom. |
| **Data Fetching** | In-memory only. Datasets load from `sklearn.datasets` built-ins or a local file in `data/`. No network calls at runtime. |
| **Rendering** | matplotlib inline backend in the notebook; `Agg` backend in scripts and tests. Figures sized for portrait Letter — max `figsize=(10, 6)`. |
| **Integrations** | None. No third-party services, no APIs, no auth. |
| **Infrastructure** | Local filesystem + Git. No containers, no cloud runtime. CI is permitted **solely** to re-run the existing Phase 0 gates (`scripts/verify_setup.py`, `pytest tests/`) on push — it adds no new methodology and no runtime dependency. See ADR 0002. |
| **Performance** | Fully vectorized. Zero Python-level iteration over arrays or DataFrames. |
| **Scalability** | Designed for datasets up to ~10,000 rows. Anything larger will not render legibly in a PDF and is out of scope. |
| **Developer Experience** | Atomic, single-purpose functions. Every non-trivial cell carries a *why* comment. Any function should be explainable via P-I-O-F without notes. |

---

## 3. Data Models

### Primary working structures

```python
# Feature matrix — the NumPy view
feature_matrix : np.ndarray      # shape (n_samples, n_features), dtype float64

# Feature table — the pandas view
df : pd.DataFrame                # shape (n_samples, n_features + labels)
                                 # index: RangeIndex, contiguous, zero-based
                                 # no MultiIndex for this lab

# Column statistic — must retain 2D shape for broadcasting
column_means : np.ndarray        # shape (1, n_features)   NOT (n_features,)
```

### Invariants — always true after any transformation

| Invariant | Enforced by |
|---|---|
| `df.index` is contiguous and zero-based after any filter or merge | `check_alignment()` |
| Any vector broadcast over a matrix retains explicit 2D shape | `check_broadcasting()` |
| No `NaN`, `+inf`, or `-inf` in any numeric array entering a downstream step | `check_integrity()` |
| Min-max scaled data lies within `[0.0, 1.0]` inclusive | `check_scale()` |
| Row count never changes during a column assignment | `check_alignment()` + explicit shape comparison |

---

## 4. Interface Spec — Call Graph (Ladder Logic)

Every exercise follows the same ladder. The validator call is not optional and is not appended afterward — it precedes the transformation.

```
load_data()
    │
    ▼
PipelineValidator.check_integrity(raw)          ← gate: is the input even usable?
    │
    ▼
transform()  ── e.g. filter / merge / normalize / aggregate
    │
    ├──▶ PipelineValidator.check_alignment(df, series)    [pandas path]
    ├──▶ PipelineValidator.check_broadcasting(mat, vec)   [numpy path]
    │
    ▼
PipelineValidator.check_integrity(result)       ← gate: did the transform corrupt anything?
    │
    ▼
PipelineValidator.check_scale(result)           ← gate: only after normalization
    │
    ▼
visualize()  ── matplotlib figure with title, labels, legend
```

**Read the gates as contracts.** `check_integrity` before *and* after is deliberate: the first proves the input was clean, the second proves the transformation is what corrupted it if the second fails. Without both, a failure is ambiguous.

---

## 5. Forbidden Patterns

Reject these on sight. Each maps to a real, specific failure mode.

| Pattern | Why it is forbidden |
|---|---|
| `for i in range(len(arr)):` over array data | Defeats vectorization; the entire point of Module 2 |
| `df['col'][mask] = value` (chained assignment) | Triggers `SettingWithCopyWarning`; may modify a copy and silently do nothing |
| `arr.mean(axis=0)` fed into a subtraction without `keepdims=True` | Squeezes to shape `(n,)`; broadcasting silently produces wrong math |
| `df['new'] = filtered_series` without index reset or explicit join | Pandas index-aligns and pads mismatches with `NaN` — no warning raised |
| `df.isna().sum() == 0` as an integrity check | Misses `+inf` / `-inf`, which are equally destructive. Use `np.isfinite().all()` |
| `except: pass` or bare `except:` | Hides the failure this entire architecture exists to surface |
| Hardcoded absolute paths (`/Users/joseph/...`) | Breaks on every other machine; use `pathlib.Path(__file__).parent` |
| Personal Access Tokens or credentials in any tracked file | Security failure and an automatic professional red flag |
| `plt.show()` inside a loop generating many figures | Produces an unreviewable PDF |
| `git add .` | Stages `.venv`, checkpoints, and informal notes. Stage by explicit path. |

---

## 6. Testing Strategy

**Two layers, distinct purposes.**

| Layer | Location | Runner | Answers |
|---|---|---|---|
| Tooling tests | `tests/test_pipeline_validator.py` | `pytest` | "Does my validator actually catch what it claims to catch?" |
| Pipeline assertions | inline in notebook cells | notebook kernel | "Is *this* transformation mathematically sound?" |

The tooling layer exists because an assertion helper that silently passes on bad input is worse than no helper at all — it manufactures false confidence. Each validator method has a test that feeds it **known-bad** input and asserts that it raises.

**TDD ordering, non-negotiable:** the assertion is written before the transformation, not after. Writing it afterward makes it a description of what the code happened to do, not a contract the code must satisfy.

---

## 7. Environment & Reproducibility

- The `.venv/` directory is **never** committed. It is machine-specific and large.
- Dependencies are declared in `requirements.txt`, not installed ad hoc. If you `pip install` something, add it to the file in the same commit or it does not exist.
- The notebook kernel must be explicitly bound to `.venv`, not the system Python. Verify in Cursor's kernel dropdown, top-right of the notebook pane.
- `scripts/verify_setup.py` is the reproducibility gate. It must exit `0` before any lab work begins.

---

## 8. Amendment Log

Architectural decisions change. When they do, record it here rather than silently editing the section above.

| Date | Change | Reason | RCA class |
|---|---|---|---|
| 2026-08-20 | Initial specification | Project scaffold | — |
