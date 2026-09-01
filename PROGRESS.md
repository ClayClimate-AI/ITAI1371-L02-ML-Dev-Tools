# L02 Progress Log

**Governing sentence:** Test before code. Spec before implementation. Human checkpoint before every advance.

## Current state
- **Phase:** Harvest / submission prep
- **Last completed:** Harvest step 3 — Joseph's reflective journal committed (`0686bc8`, 2026-09-01)
- **Next step:** Harvest step 4 — Joseph's contribution journal (D3); then aggregate any teammate PDFs received by Canvas and submit the GitHub link on Canvas (due Tue Sep 2, 11:59 PM)
- **Environment:** .venv | verify_setup: PASS | pytest: PASS (18) | notebook `[1]`→`[7]` clean
- **Notebook canonical path:** `src/Module_02_Lab_Exercise.ipynb` (moved back to `src/` 2026-08-31; the 2026-08-28 move to root was reversed)

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
| H | Cell 14 — Markdown reflection | FILL-IN placeholders replaced with real content; no code cells touched; content matches human-approved draft exactly | Human-authored (via C1-approved draft) | PASS | db2733a | Dataset Overview, Key Findings, Questions, Reflection sections written per approved draft; confirmed by human review of rendered cell |

## Harvest log
| Step | Description | Validated | Commit | Notes |
|------|-------------|-----------|--------|-------|
| 1 | Clean full notebook run (Restart-equivalent Run All via `nbconvert --execute --inplace`) | PASS | 2d36496 | Exit code 0; no cell error outputs (verified by scanning notebook JSON); execution counts 1→7 in order across cells 2,4,5,7,9,12,13; plot outputs present for Cells 7 and 13 |
| 2 | PDF export → `deliverables/L02_TuringCollective_ITAI1371.pdf` | PASS | 8c110c7 | Regenerated via `nbconvert --to html` → `white-space:pre-wrap` CSS injected into `<head>` → headless Chrome `--print-to-pdf --no-pdf-header-footer`. C5 visual audit PASS: 10 pp, no code clipping (all previously-clipped lines now wrap), both plots whole and unsplit, counters [1]→[7], syntax highlighting preserved, no browser header/footer, no `file:///` path. Superseded ad-hoc PDF `L02_Turing_Collective_ITAI1371.pdf` (wrong name, footer path, clipped code) — deleted, never committed. Notebook re-execute produced timestamp-only diff → reverted (content identical to 2d36496). |
| 3 | Reflective Journal → `deliverables/journals/L02Journal_JosephClay_ITAI1371.pdf` | PASS | 0686bc8 | 2-page reflection, interview-sourced (C6). Covers all 5 rubric elements; no step-by-step narration. Two earlier drafts rejected: v1 misattributed *The Guardrail Blueprint* as an HCC resource (fixed); v2 added 3 fabricated external citations — Salami/Simplico/Autonoma AI (removed). Final version cites nothing external. |
| 4 | Contribution Journal → `deliverables/contributions/L02Contribution_JosephClay_ITAI1371.pdf` | — | — | Not started. Factual account, not reflective. 20 pts; "no individual contribution = -20". |

## Session handoffs
### 2026-08-25
- Done: repo structure clean and pushed; system operating files local; template v1.1 locked; Phase 0 gates run — verify_setup.py PASS, pytest 18/18 PASS; CI workflow added and passing (ADR 0002); Unit A (Cell 2 — Imports) PASS after adding scikit-learn dependency (ADR 0001); Unit B (Cell 4 — load_iris) PASS; Unit C (Cell 5 — DataFrame) PASS; Unit D (Cell 7 — scatter plot) PASS; Unit E (Cell 9 — groupby stats) PASS; Unit F (Cell 12 — Task 1) PASS; Unit G (Cell 13 — Task 2) PASS; Unit H (Cell 14 — markdown reflection) PASS; Harvest step 1 (clean full run) PASS
- Blocked: none
- Next exact action: Harvest step 2 — PDF export (not started; awaiting go-ahead). Do not write journals yet.

### 2026-08-27
- Done: OQ-1 resolved — group name "The Turing Collective", filename token `TuringCollective`; Canvas "File Naming Convention" confirmed as authoritative (`L02_<Token>_ITAI1371.pdf`, `L02Journal_<Token>_ITAI1371.pdf` — no `_` after `L02`). Corrected filename patterns + stale `[16]`→`[7]` cell-counter refs across Product_Spec.md, README.md, docs/reflective-journal.md (tracked) and docs/pdf-export-guide.md, docs/submission-runbook.md (gitignored engine files). **Harvest step 2 PASS** — regenerated `deliverables/L02_TuringCollective_ITAI1371.pdf`, C5 visual audit clean; deleted superseded ad-hoc `L02_Turing_Collective_ITAI1371.pdf`.
- Blocked: none
- Open flags for Pilot: (1) ~~notebook path mismatch~~ **RESOLVED 2026-08-28** — `git mv` to repo root as `Module_02_Lab_Exercise.ipynb` (singular, matches Canvas); all doc refs realigned; (2) `.gitignore` keeps AGENTS.md/CLAUDE.md/prompt-history.md/submission-runbook.md/pdf-export-guide.md/naming-conventions.md/session-kickoff-prompt.md local — Pilot decision 2026-08-28: **keep gitignored** (no authoritative requirement to publish engine files; only the 3 documents + git link are required); (3) PR #1 self-merge (entry 001) still uncorrected.

### 2026-08-28
- Done: **notebook-move reconcile** — `git mv src/Module_02_Lab_Exercise.ipynb` → repo root; realigned README.md, docs/environment-setup.md, scripts/verify_setup.py, docs/submission-runbook.md (gitignored). **CI-governance reconcile** — CI workflow (`ad12277`) contradicted `Tech_Spec.md` §2 Infrastructure ("No CI") with no paper trail; amended Tech_Spec to carve out read-only Phase 0 gate automation (cites ADR 0002), added `.github/` + `docs/adr/` to the README repo map + a "gates run in CI" sentence, logged prompt-history entry [010].
- Blocked: none
- Next exact action: Harvest step 3 — Reflective Journal. Interview the Pilot; do not draft it. Source: docs/reflective-journal.md.

### 2026-08-31 (separate session — reconstructed)
- Done: notebook moved back to `src/Module_02_Lab_Exercise.ipynb` (canonical); `deliverables/` restructured into `notebooks/` `journals/` `contributions/` for per-member PDFs; `docs/L02-TEAM-PDF-INTAKE.md` added; `docs/project-template.md` and `docs/comprehensive-breakdown.md` created and gitignored (`6bb4a8a`, `629c514`). Teammate activity: Yilin Leng self-merged PRs #2–#4 (files landed at repo root, misnamed) — later moved into subfolders and root copies removed (`aa7749e`, `93738c1`); Alexander Debusk's 3 PDFs added. PRs #4 (Yilin) merged; Alex #4 / Shareefah #5 closed unmerged. Prof. Rao (Aug 30) changed teammate intake to Canvas message + manual upload, deadline extended to Tue Sep 2.
- Blocked: none

### 2026-09-01
- Done: **D2 reflective journal** interview (C6) + committed `deliverables/journals/L02Journal_JosephClay_ITAI1371.pdf` (`0686bc8`). **Full repo audit** + fixes: gitignored `checkpoint.md` and `The_Guardrail_Blueprint.pdf`; refreshed `checkpoint.md` (was stale); rewrote `docs/L02-TEAM-PDF-INTAKE.md` for the Canvas-message process (PR path kept as record); updated README deliverables section; this log. Repo hygiene verified — no secrets/junk tracked, engine files all gitignored, `requirements.txt` matches notebook imports, gates green.
- Blocked (needs Pilot / permission): (a) delete 4 stale remote branches — `git push --delete` blocked by classifier, do via GitHub UI or approve the command; branch `Shareefah-Lab-patch-1` deliberately NOT deleted (holds `LO2_SHAREEFAH_ITAI.pdf`, her only submission, unmerged); (b) remove collaborator access (needs `gh` auth or GitHub UI).
- Next exact action: D3 — Joseph's contribution journal.
