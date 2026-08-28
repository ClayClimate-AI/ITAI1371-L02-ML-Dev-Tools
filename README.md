# ITAI-1371 — L02: Machine Learning Development Tools

> **Course:** ITAI-1371 Introduction to Machine Learning — Houston Community College
> **Module:** 2 — Essential Development Environment (pandas, NumPy, matplotlib)
> **Environment:** Cursor / VS Code + local Python virtual environment + Git
> **Deadline:** August 30, 11:59 PM
> **Points:** 100
> **Method:** Spec-driven development — specs written before code, defensive validation before analysis

---

## What this repository is

This is not a folder of homework files. It is a **spec-anchored workspace**: the specification declares intent, the notebook merely realizes it. Every artifact here exists to make the work verifiable — by me, by a teammate, by an instructor, or by an AI agent picking the project up cold.

**Problem → Value → Feature**

| Layer | Statement |
|---|---|
| **Problem** | Notebook-based ML work drifts. Cells run out of order, silent `NaN`s corrupt data without raising errors, and reflective writing collapses into "first I did X, then Y." |
| **Value** | A pipeline that is provably correct before a model ever sees the data, plus documentation that demonstrates ownership rather than narration. |
| **Feature** | 16 vectorized exercises, guarded by four defensive assertions, exported to clean PDFs, backed by a reflective journal grounded in real debugging. |

---

## Quick start

```bash
# 1. Create and activate the virtual environment
python -m venv .venv
source .venv/bin/activate          # macOS / Linux
# .venv\Scripts\activate           # Windows CMD
# .venv\Scripts\Activate.ps1       # Windows PowerShell

# 2. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 3. Verify the environment before touching the notebook
python scripts/verify_setup.py

# 4. Confirm the validator itself is sound
pytest tests/ -v
```

If `verify_setup.py` exits non-zero, **stop**. Do not start the lab on a broken environment.

---

## Repository map

```
ITAI1371-L02-ML-Dev-Tools/
│
├── README.md                       # You are here — human entry point
├── Product_Spec.md                 # WHY + WHAT: intent, Gherkin acceptance criteria
├── Tech_Spec.md                    # HOW: architectural boundaries, 9 pillars, call graph
├── requirements.txt                # Pinned dependency set
├── .gitignore
│
├── Module_02_Lab_Exercises.ipynb   # THE DELIVERABLE — 16 exercises
│
├── src/
│   └── pipeline_validator.py       # PipelineValidator — the four defensive checks
│
├── tests/
│   └── test_pipeline_validator.py  # Proves the validator catches what it claims to
│
├── scripts/
│   └── verify_setup.py             # Environment gate — run before any lab work
│
├── docs/
│   ├── environment-setup.md        # Full local setup walkthrough
│   ├── tdd-assertion-guide.md      # Why each assertion exists (the deep reasoning)
│   ├── debugging-odyssey.md        # Working bug log — feeds Journal Section 2
│   └── reflective-journal.md       # Journal draft source → exports to PDF
│
└── deliverables/                   # Final PDFs, named per instructor spec
```

---

## Required deliverables

| Deliverable | Exact filename | Location |
|---|---|---|
| Raw notebook | `Module_02_Lab_Exercises.ipynb` | repo root |
| Notebook PDF | `L02_TuringCollective_ITAI1371.pdf` | `deliverables/` |
| Reflective journal PDF (1–2 pages) | `L02Journal_TuringCollective_ITAI1371.pdf` | `deliverables/` |

> **Group name confirmed** (Pilot, 2026-08-27): "The Turing Collective", filename token `TuringCollective` (OQ-1 resolved). Filenames follow the Canvas "File Naming Convention" section character for character — note the journal file has **no underscore after `L02`** (`L02Journal_…`, not `L02_Journal_…`). Instructor-mandated filenames are the one place where this repo's own naming rules do **not** apply.

---

## Working method

Work proceeds one exercise at a time: specify, implement, verify, commit. No batch dumps, no "write all 16 cells." Each defensive assertion in `pipeline_validator.py` exists for a reason documented in `docs/tdd-assertion-guide.md`, and each real bug hit along the way is logged in `docs/debugging-odyssey.md` rather than silently fixed.

---

## Where to start reading

1. [`Product_Spec.md`](Product_Spec.md) — what "done" means, in Gherkin
2. [`Tech_Spec.md`](Tech_Spec.md) — the boundaries the code may not cross
3. [`docs/tdd-assertion-guide.md`](docs/tdd-assertion-guide.md) — why the four assertions exist

---

*Engineering Pilot: Joseph Clay. The specification is the source of truth; the code realizes it.*
