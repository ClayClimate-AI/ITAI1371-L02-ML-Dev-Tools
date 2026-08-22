# TDD Assertion Guide

Why each of the four defensive checks in `src/pipeline_validator.py` exists, what failure it prevents, and why the specific syntax was chosen over the obvious alternative.

**This document is the reasoning. The executable lives in `src/pipeline_validator.py`.** Code in a markdown fence cannot be imported, tested, or version-controlled meaningfully — so it does not live here. When the implementation changes, update both.

---

## The governing idea

Every check below guards a **silent** failure — one that produces no error at the moment of corruption. That is the whole category. A loud failure is a gift; you find it immediately. A silent one trains successfully on corrupted data and you discover it in production, or never.

**TDD ordering is not optional:** write the assertion *before* the transformation. Written afterward, an assertion describes what the code happened to do. Written before, it is a contract the code must satisfy. Same three lines, entirely different epistemic status.

---

## 1. Index Alignment — the silent killer of pandas assignments

```python
PipelineValidator.check_alignment(df, series, label="Feature")
```

### What it proves
The row indices of the target DataFrame and the incoming Series are identical *and in the same order*.

### The failure it prevents
**In pandas, data alignment is governed by index labels, not row positions.**

Filter, shuffle, or drop rows and pandas retains the original labels — you get index `[0, 2, 5]`, not `[0, 1, 2]`. Assign that Series back into a frame indexed `[0, 1, 2]` and pandas looks for label `5`, does not find it, and **silently fills the mismatch with `NaN`.** No warning. No exception. The cell runs green.

### Why not `len(a) == len(b)`?
This is the rookie version and it does not work. Two Series of length 100 — one indexed `0-99`, one indexed `1-100` — pass a length check and still corrupt on assignment. `.index.equals()` performs an order-sensitive, element-wise comparison at C level. It is both stricter and faster.

### Downstream ML impact
Silent `NaN`s do not surface where they are created. They surface hours later inside `.fit()` as a cryptic traceback, or — worse — get imputed by a later cleaning step and train a model on fabricated values. This check isolates data-pipeline bugs from model bugs, which are otherwise nearly impossible to tell apart.

---

## 2. Broadcasting Shape — proving the math, not just survival

```python
PipelineValidator.check_broadcasting(feature_matrix, column_means, axis=0)
```

### What it proves
A statistic vector retains explicit 2D shape and will broadcast over the matrix in the intended direction.

### The failure it prevents
`feature_matrix.mean(axis=0)` returns shape `(cols,)` — NumPy squeezes the result to 1D by default. Subtract that from a `(rows, cols)` matrix and NumPy's broadcasting rules will often *stretch it anyway*, producing a result of the correct shape containing **the wrong numbers**.

```python
# WRONG — squeezed to (cols,), broadcasts along the wrong axis
normalized = matrix - matrix.mean(axis=1)

# CORRECT — retains (rows, 1), broadcasts as intended
normalized = matrix - matrix.mean(axis=1, keepdims=True)
```

### Why not `try/except`?
A `try/except` block only catches a hard crash. This bug does not crash. The code runs, the shapes look plausible, the numbers are wrong. **Explicit shape assertions prove mathematical correctness; exception handling only proves code survivability.** Those are different claims and only one of them is what you need.

### Downstream ML impact
Vectorized operations run on C-compiled loops rather than the Python interpreter — often 50–100× faster on array workloads. But speed is worthless if the dimensions are wrong. In a neural network forward pass, an incorrectly broadcast weight matrix silently corrupts every activation downstream without raising a single error.

---

## 3. Numerical Integrity — NaN *and* infinity

```python
PipelineValidator.check_integrity(data, name="Normalized features")
```

### What it proves
No `NaN`, `+inf`, or `-inf` anywhere in the array.

### The failure it prevents
Division by a near-zero value produces `inf`. `log(0)` produces `-inf`. Null propagation produces `NaN`. All three arise naturally from ordinary preprocessing — scaling, log transforms, ratio features — and none of them raise at the point of creation.

### Why `np.isfinite().all()` and not `df.isna().sum() == 0`?
The common version **misses infinities entirely.** `.isna()` returns `False` for `inf` — it is a perfectly valid float as far as pandas is concerned. And `inf` destroys a gradient exactly as thoroughly as `NaN` does.

`np.isfinite()` is a single vectorized pass catching `NaN`, `+inf`, and `-inf` together. `.all()` reduces it to one boolean.

### Downstream ML impact
Feed `NaN` into a loss calculation and the loss becomes `NaN`. Once the loss is `NaN`, **every gradient in the backward pass becomes `NaN`, and every weight in the network is overwritten with `NaN` on the next update.** The model is destroyed in a single step and reports no error while doing it.

### Ordering constraint
Run integrity **before** scale. `min()` and `max()` on an array containing `NaN` return `NaN`, and every comparison against `NaN` evaluates `False` — so the scale check would fail with a message pointing at the wrong problem.

---

## 4. Scale Boundary — proving normalization normalized

```python
PipelineValidator.check_scale(normalized, min_val=0.0, max_val=1.0)
```

### What it proves
Every value falls within the intended range, inclusive of the endpoints.

### The failure it prevents
Features arrive on wildly different scales — age spans `0–100`, income spans `10,000–1,000,000`. Feed those raw into a distance-based model (KNN) or a gradient-descent model and **income dominates the objective entirely**; age contributes essentially nothing regardless of how predictive it is.

Min-max scaling fixes this — when it works. The usual silent failure is a zero-range column (every value identical), which produces a division by zero and yields `NaN` or `inf` rather than a scaled value.

### Why report the actual bounds in the message?
When an assertion fails you need to know *by how much*. `[0.0000, 1.0003]` is a floating-point rounding artifact. `[0.0000, 47.3021]` means the denominator is wrong. Same failure, completely different fix — and the error message should tell you which one you have without requiring a debugging session.

### Downstream ML impact
Normalized features produce a loss surface that is roughly spherical rather than a long narrow valley. Gradient descent converges in dramatically fewer steps. Unnormalized features produce a surface where the optimizer oscillates across the narrow axis and crawls along the long one.

---

## Reference — inline assertions

For quick checks inside a notebook cell where importing the full validator is overkill:

```python
# Shape
assert a.shape == b.shape, f"Dimension mismatch: {a.shape} vs {b.shape}"

# Integrity (catches NaN and inf together)
assert np.isfinite(data).all(), "Invalid values detected in pipeline"

# Required columns present
required = {"age", "income", "target"}
assert required.issubset(df.columns), f"Missing features. Found: {list(df.columns)}"

# Row count preserved through a merge
assert before.shape[0] == after.shape[0], "Row count changed during column merge"

# Scale
assert data.min() >= 0.0 and data.max() <= 1.0, f"Range is [{data.min():.4f}, {data.max():.4f}]"
```

**Prefer the validator** for anything guarding a real transformation — it produces diagnostic messages that name the fix, and it is itself under test in `tests/test_pipeline_validator.py`.

---

## The meta-point

`tests/test_pipeline_validator.py` exists because **an assertion helper that silently passes on bad input is worse than having no helper at all.** It manufactures confidence, which is the one thing more dangerous than doubt.

Each validator method has at least one test that feeds it known-bad input and asserts it raises. That is what makes the checks trustworthy rather than decorative.
