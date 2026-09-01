# L02 Contribution Journal

**Student:** Joseph Clay  
**Group:** The Turing Collective  
**Course:** ITAI-1371 — Machine Learning Development Tools  
**Date:** 2026-09-01  
**Repository:** https://github.com/ClayClimate-AI/ITAI1371-L02-ML-Dev-Tools  

This is a factual account of work performed for the group submission. It is not a reflective essay.

---

## 1. Team communication and coordination

- Proposed the group name **The Turing Collective** and coordinated the prerequisite Git assignment before lab implementation began.
- Authored and distributed a Collaborative Git Playbook so teammates had one authoritative workflow instead of conflicting chat instructions.
- **Created Slack channels** for the group, **offered help** there for access paths (fork vs collaborator invite), deadlines, and naming, then **closed those Slack channels** when that channel stopped being the right place to work.
- After Prof. Rao’s 2026-08-30 process change, **moved team communication to Canvas messages**: teammates send their three PDFs to Joseph; Joseph commits them and submits the public GitHub link.
- Documented that process in `docs/L02-TEAM-PDF-INTAKE.md` (filenames, folders, Monday hand-off, Tuesday Canvas link).
- Removed collaborator write access once intake moved to Canvas, so the graded tree on `main` stays controlled.

---

## 2. Repository ownership and infrastructure

Git shortlog on this repo attributes the large majority of commits to Joseph Clay (scaffold through harvest). Concrete ownership includes:

| Area | What was delivered |
|---|---|
| Specs | `Product_Spec.md`, `Tech_Spec.md`, acceptance criteria, open-question tracking (OQ-1 group token resolved) |
| Environment gates | `.venv`, `requirements.txt` (including scikit-learn per ADR 0001), `scripts/verify_setup.py`, pytest suite for `PipelineValidator` (18 tests) |
| CI | `.github/workflows/ci.yml` — Phase 0 gates only (ADR 0002); Tech Spec amended so CI is an explicit carve-out |
| Lab notebook | Units A–H executed and logged in `PROGRESS.md`; clean run `[1]`→`[7]`; PDF export path established |
| Deliverables layout | `deliverables/notebooks/`, `journals/`, `contributions/` with per-member `FirstLast` naming |
| Methodology artifact | `The_Guardrail_Blueprint.pdf` — layered guardrail model used to run the lab (published in-repo for the instructor) |
| Hygiene | Root PDF strays removed; Yilin files moved from repo root into the correct subfolders; README / intake docs kept aligned with Canvas |

---

## 3. Individual graded artifacts (Joseph)

| Deliverable | Path | Status |
|---|---|---|
| Notebook PDF | `deliverables/notebooks/L02_JosephClay_ITAI1371.pdf` | Complete |
| Reflective journal PDF | `deliverables/journals/L02Journal_JosephClay_ITAI1371.pdf` | Complete |
| Contribution journal PDF | `deliverables/contributions/L02Contribution_JosephClay_ITAI1371.pdf` | This document |

---

## 4. Teammate PDF intake (as of 2026-09-01)

| Member | Notebook | Journal | Contribution |
|---|---|---|---|
| Joseph Clay | Yes | Yes | Yes |
| Alexander Debusk | Yes | Yes | Yes |
| Yilin Leng | Yes (filename has spaces — left as submitted) | Yes | Yes (filename has spaces — left as submitted) |
| Shareefah | Pending Canvas message | Pending | Pending |

No Shareefah files are on `main` until her three PDFs arrive via Canvas and are placed under `deliverables/`. Stale remote branches from the retired PR intake path are deleted so the submitted link points at a clean branch set.

---

## 5. Summary

Contribution was both **technical** (specs, gates, validator tests, CI, notebook execution, PDF harvest, repo hygiene) and **operational** (Slack standup then close-out, Canvas intake, collaborator removal, teammate file placement). The only external dependency left for a complete twelve-PDF set is Shareefah’s three Canvas submissions.
