# Product_Spec.md

> **Phase 0 — SPECIFY.** This document owns the *why* and the *what*. It does not describe implementation. If a decision here conflicts with anything in `Tech_Spec.md`, this file wins and the tech spec gets amended.

---

## 1. Customer Intent

**Who:** A first-semester machine learning student operating as Engineering Pilot, working locally in Cursor rather than in a browser notebook.

**Root problem:** Notebook work rots. Cells execute out of order and produce results that cannot be reproduced. Pandas silently pads mismatched indices with `NaN` instead of raising. NumPy quietly squeezes a dimension and broadcasts the wrong way. None of these throw an error at the moment they occur — they surface hours later as a cryptic traceback inside `.fit()`, or worse, as a model that trains successfully on corrupted data.

**What is actually being built:** Not "16 completed exercises." A **verifiable data pipeline** where every transformation is preceded by a check that proves the transformation is mathematically sound, plus the documentation that demonstrates the Pilot understands why each check exists.

**Why it matters beyond the grade:** These four assertion patterns are the same ones used in production ML pipelines. Learning them on a 150-row Iris dataset costs nothing. Learning them on a live system costs a job.

---

## 2. User Stories

| # | Story |
|---|---|
| **US-1** | As the Pilot, I need a one-command environment check so I know the failure is in my code, not my install. |
| **US-2** | As the Pilot, I need every transformation guarded by an assertion so silent corruption becomes a loud, immediate failure. |
| **US-3** | As the Pilot, I need every bug captured *at the moment it happens*, because by the time I write the journal I will have forgotten what I actually believed before the error. |
| **US-4** | As the Pilot, I need PDFs that export cleanly on the first try, because a clipped chart costs points that the underlying work earned. |
| **US-5** | As the Pilot, I need a reflective journal that is analytical rather than chronological, because the rubric penalizes narration. |
| **US-6** | As a teammate or instructor, I need to open this repository cold and understand the state of the work within two minutes. |
| **US-7** | As an AI agent, I need explicit boundaries so I do not over-engineer, add unrequested dependencies, or dump code the Pilot cannot defend. |

---

## 3. Acceptance Criteria (Gherkin)

These are binary. Each either passes or does not. There is no partial credit at the spec level.

### Environment

```gherkin
Scenario: Environment gate passes before lab work begins
  Given a fresh clone of the repository
  When I create a .venv, install requirements.txt, and run scripts/verify_setup.py
  Then every dependency check reports PASS
  And every functional check reports PASS
  And the script exits with code 0

Scenario: Environment gate blocks work on a broken install
  Given matplotlib is not installed in the active environment
  When I run scripts/verify_setup.py
  Then the script reports the missing library by name
  And prints the exact pip command needed to fix it
  And exits with a non-zero code
```

### Notebook execution

```gherkin
Scenario: Notebook runs clean from a cold kernel
  Given the notebook is bound to the .venv kernel
  When I select "Restart Kernel and Run All Cells"
  Then all 16 exercises execute without raising
  And the execution counters read [1] through [16] in unbroken sequence
  And no cell output exceeds 40 printed lines

Scenario: A transformation is attempted without a guard
  Given an exercise that modifies array shape or DataFrame structure
  When the cell contains no preceding PipelineValidator check
  Then the exercise is considered incomplete regardless of whether it runs
```

### Vectorization

```gherkin
Scenario: Array operations avoid Python-level iteration
  Given any exercise that operates elementwise across an array or column
  When the code is reviewed against Tech_Spec.md
  Then it contains no for-loop or while-loop over the data
  And uses a vectorized NumPy or pandas operation instead
```

### Visualization

```gherkin
Scenario: A figure is submission-ready
  Given any matplotlib figure in the notebook
  When the figure is rendered
  Then it has a title, labeled axes, and a legend if more than one series is plotted
  And no tick labels, legend entries, or titles overlap
  And the figure fits within portrait Letter margins when exported
```

### Debugging capture

```gherkin
Scenario: A bug is logged before it is fixed
  Given an assertion fails or a traceback is raised
  When I begin troubleshooting
  Then a new entry is opened in docs/debugging-odyssey.md
  And the Spec, Test, and Crash sections are filled in before the fix is applied
  And the Resolution section is completed after the fix passes

Scenario: The journal has enough raw material
  Given the journal is ready to be drafted
  When docs/debugging-odyssey.md is reviewed
  Then it contains at least two fully completed bug logs
```

### Deliverables

```gherkin
Scenario: Deliverables are correctly named and located
  Given the lab and journal are complete
  When I inspect the deliverables/ directory
  Then it contains L02_<GroupName>_ITAI1371.pdf
  And it contains L02_Journal_<GroupName>_ITAI1371.pdf
  And <GroupName> exactly matches the group name registered on Canvas

Scenario: The journal is reflective, not descriptive
  Given the completed reflective journal
  When any paragraph is read in isolation
  Then it analyzes a shift in understanding, a trade-off, or a consequence
  And it contains no chronological narration ("first I... then I...")
  And it contains no textbook definitions of pandas, NumPy, or matplotlib
  And the rendered PDF is between 1 and 2 pages
```

### Version control

```gherkin
Scenario: Commit history proves incremental orchestration
  Given the completed project
  When git log is reviewed
  Then each commit represents one logical change
  And no commit adds more than one exercise
  And no commit message is generic ("update", "fix stuff", "wip")
  And no secrets, .venv contents, or informal notes appear in any commit
```

---

## 4. Out of Scope

Explicitly **not** part of L02. If an agent proposes any of these, it is freestyling — reject it.

- Training, fitting, or evaluating any model
- scikit-learn, seaborn, plotly, or any dependency beyond `requirements.txt`
- Persistent storage, databases, or external APIs
- Interactive dashboards or web output
- Datasets larger than will comfortably render in a PDF

---

## 5. Success Metrics — Outcomes, Not Output

Retired metrics (output): cells completed, lines written, hours logged.

| North Star | Target | How it is measured |
|---|---|---|
| **Pipeline integrity** | Zero silent `NaN`s reach any downstream step | All four `PipelineValidator` checks pass on every guarded transformation |
| **Reproducibility** | 100% clean cold run | Restart-and-run-all completes `[1]`–`[16]` with no manual intervention |
| **Technical ownership** | Pilot can P-I-O-F any function in the notebook without notes | Self-test before submission |
| **Documented pushback** | ≥ 2 logged instances of challenging or refactoring AI output | `prompt-history.md` |
| **Debugging depth** | ≥ 2 complete bug logs with root cause identified | `docs/debugging-odyssey.md` |
| **Grade** | 100 / 100 | Canvas |

---

## 6. Open Questions

Track unresolved items here rather than guessing. An agent encountering an open question must stop and ask.

| ID | Question | Status | Owner |
|---|---|---|---|
| OQ-1 | Final group name for deliverable filenames — "Turing Collective" proposed, unconfirmed | **OPEN** | Pilot / team |
| OQ-2 | Does the instructor require the 16 exercises in the assignment's original order? | **OPEN** | Pilot — verify on Canvas |
| OQ-3 | Is the notebook submitted via GitHub link, Canvas upload, or both? | **OPEN** | Pilot — verify on Canvas |

> **Rule:** No deliverable PDF is generated while OQ-1 is open. Renaming a submitted file is not always possible.
