# Environment Setup

Full local setup for ITAI-1371 L02 in Cursor / VS Code. Read `README.md` first for the quick start; this document is the detailed version and the troubleshooting reference.

---

## Prerequisites

| Requirement | Source | Verify with |
|---|---|---|
| Cursor or VS Code | official site | opens |
| Python 3.10+ (3.8 minimum) | [python.org](https://www.python.org/downloads/) | `python --version` |
| Git | [git-scm.com](https://git-scm.com/downloads) | `git --version` |
| GitHub account | [github.com](https://github.com/join) | — |

> **Windows:** during Python installation, check **"Add Python to PATH."** Skipping it is the single most common cause of `python: command not found` later.

---

## Step 1 — Extensions

Extensions view (`Ctrl+Shift+X` / `Cmd+Shift+X`), install both:

- **Python** (Microsoft)
- **Jupyter** (Microsoft) — enables `.ipynb` support

---

## Step 2 — Open the project

**File → Open Folder**, select the repository root. Not a parent folder, not a subfolder. Cursor's `@` file references and the integrated terminal both resolve relative to whatever you open here.

---

## Step 3 — Virtual environment

Open the integrated terminal (`` Ctrl+` `` / `` Cmd+` ``).

```bash
python -m venv .venv
```

Activate it:

**macOS / Linux**
```bash
source .venv/bin/activate
```

**Windows — Command Prompt**
```cmd
.venv\Scripts\activate
```

**Windows — PowerShell**
```powershell
.venv\Scripts\Activate.ps1
```

Your prompt should now be prefixed with `(.venv)`. If it is not, activation failed — do not proceed.

> **PowerShell blocks the script?** If you see *"running scripts is disabled on this system,"* run:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```
> This affects your user account only, not the machine.

**Why this matters:** without isolation, `pip install pandas` writes to system Python. A different project needing a different pandas version then breaks this one, and the failure appears as an unrelated error inside your notebook weeks later.

---

## Step 4 — Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Never `pip install` a package without adding it to `requirements.txt` in the same commit. An undeclared dependency works on your machine and fails on everyone else's — the definition of an unreproducible build.

---

## Step 5 — Verify before you build

```bash
python scripts/verify_setup.py
```

Expected final lines:

```
[OK] Environment verified. You are cleared to open
     Module_02_Lab_Exercise.ipynb and bind the .venv kernel.
```

**If it exits non-zero, stop.** The whole point of this gate is to remove ambiguity: if the environment is verified and something then breaks, the bug is in your code. Without the gate, every error has two possible causes and you will waste hours on the wrong one.

Confirm the exit code explicitly if you want to be certain:

```bash
python scripts/verify_setup.py; echo "exit: $?"     # macOS/Linux
python scripts\verify_setup.py & echo exit: %ERRORLEVEL%   # Windows CMD
```

---

## Step 6 — Confirm the tooling is sound

```bash
pytest tests/ -v
```

All tests must pass. These verify that the `PipelineValidator` checks actually *fail* on bad input — an assertion helper that silently passes is worse than no helper, because it manufactures confidence.

---

## Step 7 — Bind the notebook kernel

This step is skipped more often than any other, and it is the cause of the most confusing failure mode in the entire project.

1. Open `Module_02_Lab_Exercise.ipynb`
2. Click the kernel selector, **top-right** of the notebook pane
3. Choose **Python Environments** → the interpreter inside `.venv`
4. Confirm the selector displays `.venv` and not a system or global Python

**The failure mode:** your terminal shows `(.venv)` active with pandas installed, but the notebook is bound to system Python without it. You get `ModuleNotFoundError: No module named 'pandas'` in a cell while `pip list` in the terminal clearly shows pandas installed. Hours disappear here. Check the kernel first.

Verify inside a notebook cell:

```python
import sys
print(sys.executable)   # must contain '.venv'
```

---

## Step 8 — Git identity

```bash
git config --global user.name "Joseph Clay"
git config --global user.email "your-student-email@example.com"
```

Use the email associated with your GitHub account, or commits will not attribute to your profile — which matters when the instructor grades via the GitHub audit log.

**Authentication:** use SSH keys or the Git Credential Manager. **Never** paste a Personal Access Token into a tracked file. A leaked token in commit history persists even after you delete the line — rewriting history is the only fix, and it is a bad afternoon.

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `python: command not found` | Python not on PATH | Reinstall with "Add to PATH" checked; or use `python3` on macOS/Linux |
| `(.venv)` missing from prompt | Activation failed silently | Re-run the activation command for your exact shell |
| `ModuleNotFoundError` in notebook, package installed in terminal | Kernel bound to the wrong interpreter | Step 7 |
| PowerShell refuses to run activate | Execution policy | `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` |
| `UnicodeEncodeError` in a script | Windows cp1252 console meets non-ASCII output | Project scripts are ASCII-only by design; if a third-party tool does this, set `PYTHONIOENCODING=utf-8` |
| Kernel dies immediately on run | Memory exhaustion or corrupt install | Restart kernel; if it persists, delete `.venv` and rebuild from Step 3 |
| `pytest: command not found` | pytest installed outside the venv | Activate the venv, reinstall requirements, or run `python -m pytest` |
| Plots render blank in the notebook | Backend set to `Agg` somewhere | `Agg` is for scripts only; the notebook should use the default inline backend |

---

## Rebuilding from scratch

When the environment is unrecoverable, do not debug it. Rebuild — it takes ninety seconds:

```bash
deactivate                     # if currently active
rm -rf .venv                   # rmdir /s .venv on Windows
python -m venv .venv
source .venv/bin/activate      # or the Windows equivalent
pip install --upgrade pip
pip install -r requirements.txt
python scripts/verify_setup.py
```

This is exactly why `.venv/` is gitignored and `requirements.txt` is tracked. The environment is disposable; the declaration of it is not.
