# Debugging Odyssey — Working Bug Log

Structured record of every significant bug encountered in L02. This feeds **Section 2 of the reflective journal**, which is the highest-scoring section of the assignment.

---

## Why this is written *during*, not after

You will not remember what you believed before the error. That is the entire problem.

Within an hour of fixing a bug, your memory rewrites itself into "I knew it was a shape issue." You did not. You thought it was something else, and the gap between what you assumed and what was actually true **is the reflective content the rubric rewards.** Descriptive writing ("I got an error and fixed it") scores near zero. The mental-model correction is what scores.

**Protocol — Checkpoint C3:** fill in *The Spec*, *The Test*, and *The Crash* **before applying the fix.** Fill in *The Resolution* after. Not the other way around.

---

## The four-stage framework

```
┌────────────────────────────────────────────┐
│  1. THE SPEC                               │  What SHOULD the data look like?
│     Expected shape, dtype, row count       │  Define it before you look.
└──────────────────┬─────────────────────────┘
                   ▼
┌────────────────────────────────────────────┐
│  2. THE TEST                               │  Write the assertion that would
│     Assertion written BEFORE the fix       │  have caught this automatically.
└──────────────────┬─────────────────────────┘
                   ▼
┌────────────────────────────────────────────┐
│  3. THE CRASH                              │  What actually happened, and
│     Traceback + root cause + what I assumed│  what did I wrongly believe?
└──────────────────┬─────────────────────────┘
                   ▼
┌────────────────────────────────────────────┐
│  4. THE RESOLUTION                         │  The fix, the RCA class, and
│     Fix + RCA + downstream ML consequence  │  what it protects downstream.
└────────────────────────────────────────────┘
```

**Minimum for the assignment: two complete logs.** Aim for three — the third is usually the most interesting, because by then you are hunting rather than flailing.

---

## Entry Template

```markdown
### Bug #N — [Short descriptive name]

**Exercise:** N
**Date:** YYYY-MM-DD
**RCA class:** Code failure | Spec failure

#### 1. The Spec — what should have happened
- **Goal:** [what this cell was supposed to accomplish]
- **Expected input:** structure / shape / dtype
- **Expected output:** structure / shape / dtype
- **Invariant that should hold:** [e.g. row count unchanged, no NaN introduced]

#### 2. The Test — the assertion that would have caught it
```python
# Written before the fix
assert ...
```

#### 3. The Crash — what actually happened
- **Error or wrong state:** [exact message, or describe the silent failure]
- **What I assumed it meant:** [BE HONEST — this is the highest-value line in the log]
- **What it actually meant:** [the real root cause]
- **How I isolated it:** [variable viewer, .shape/.dtypes inspection, print statements, docs, agent]

#### 4. The Resolution
- **The fix:** [what changed and why it works]
- **Before / after:**
```python
# BROKEN
...
# CORRECT
...
```
- **RCA:** Code failure (drifted from a valid spec) or Spec failure (spec was incomplete). If spec failure, note what was amended in Product_Spec.md or Tech_Spec.md.
- **Downstream ML consequence:** [what this would have destroyed if it reached a model]
- **What I now check automatically:** [the habit this produced]
```

---

## Worked example — use this as a calibration reference, not as your content

> The two entries below are illustrative. **Delete them and write your own.** They exist so you can see the level of specificity the rubric rewards.

### Bug #0 (EXAMPLE) — NumPy broadcasting shape mismatch

**Exercise:** 7 · **RCA class:** Code failure

#### 1. The Spec
- **Goal:** Center a feature matrix by subtracting the mean of each row.
- **Expected input:** `np.ndarray`, shape `(100, 5)`, dtype `float64`
- **Expected output:** identical shape `(100, 5)`, row means ≈ 0
- **Invariant:** shape unchanged; no NaN introduced

#### 2. The Test
```python
assert row_means.shape == (matrix.shape[0], 1), f"Expected column vector, got {row_means.shape}"
assert np.isfinite(centered).all(), "NaN or inf after centering"
```

#### 3. The Crash
- **Error:** `ValueError: operands could not be broadcast together with shapes (100,5) (100,)`
- **What I assumed:** that my matrix was the wrong shape — I went looking at how the data was loaded.
- **What it actually meant:** the *matrix* was fine. `.mean(axis=1)` squeezed the result from `(100, 1)` to `(100,)`. NumPy then tried to align that length-100 vector against the 5-column axis and could not.
- **How I isolated it:** printed `.shape` on both operands. Two seconds of information after twenty minutes of looking in the wrong place.

#### 4. The Resolution
- **The fix:** `keepdims=True` preserves the reduced axis as size 1 instead of dropping it.
```python
# BROKEN
centered = matrix - matrix.mean(axis=1)
# CORRECT
centered = matrix - matrix.mean(axis=1, keepdims=True)
```
- **RCA:** Code failure — the spec was clear that shape must be preserved; the implementation did not honor it.
- **Downstream ML consequence:** In this case NumPy raised. The dangerous version is when it does *not* raise — `axis=0` on a square matrix broadcasts silently and produces wrong numbers with no error at all. That version trains a model on garbage that looks fine.
- **What I now check automatically:** print `.shape` on both operands before any matrix arithmetic. Free, instant, and it would have saved the twenty minutes.

---

### Bug #0b (EXAMPLE) — pandas index misalignment introducing silent NaN

**Exercise:** 11 · **RCA class:** Spec failure

#### 1. The Spec
- **Goal:** Assign a filtered, processed column back into the main DataFrame.
- **Expected output:** shape `(500, M+1)`, zero NaN introduced
- **Invariant:** row count unchanged at 500

#### 2. The Test
```python
assert before.shape[0] == after.shape[0], "Row count changed during assignment"
assert df["new_feature"].isnull().sum() == 0, "Merge introduced NaN via index mismatch"
```

#### 3. The Crash
- **Error:** None. **That was the problem.** The cell ran green; 187 of 500 values were silently `NaN`.
- **What I assumed:** that assignment worked positionally, like a NumPy array or a spreadsheet column.
- **What it actually meant:** pandas aligns on index *labels*. My filtered Series retained its original labels — `[0, 3, 7, 12, ...]` — so pandas matched only where labels overlapped and padded the rest with `NaN`.
- **How I isolated it:** `.isnull().sum()` after the assignment. I only ran it because a later mean looked implausibly low.

#### 4. The Resolution
- **The fix:** reset the index before assigning, forcing positional alignment.
```python
# BROKEN
df["new_feature"] = filtered_series
# CORRECT
df["new_feature"] = filtered_series.reset_index(drop=True)
```
- **RCA:** **Spec failure.** `Tech_Spec.md` never stated that a filtered Series must have its index reset before reassignment. The implementation followed an incomplete spec. Amended §3 Invariants to make it explicit.
- **Downstream ML consequence:** 187 NaN in a training feature. Scikit-learn raises on `.fit()` — hours later, with a traceback pointing at the model, not at this cell. The bug and its symptom would have been separated by the entire pipeline.
- **What I now check automatically:** `.isnull().sum()` immediately after every assignment or merge. This is exactly what `PipelineValidator.check_alignment()` automates, and this bug is why it exists.

---

## Your entries

<!-- Delete the examples above once you have two real entries. Write yours below. -->

### Bug #1 — [name]

*(pending)*

---

### Bug #2 — [name]

*(pending)*
