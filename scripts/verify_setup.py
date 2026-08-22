#!/usr/bin/env python3
"""ITAI-1371 L02 -- local environment gate.

Run this BEFORE touching the notebook. If it exits non-zero, the environment is
broken and any error you hit in the lab is ambiguous: your code, or your install?
This script removes that ambiguity.

    python scripts/verify_setup.py
    echo $?        # 0 = ready, 1 = blocked

Design notes (see prompt-history.md entry 002):
  * Exits with a real status code. A gate that cannot fail is not a gate.
  * ASCII-only output. Emoji raise UnicodeEncodeError on Windows cp1252 consoles,
    which is exactly the environment most likely to be broken.
  * Functional checks exercise the real failure modes, not trivially-true ones.
"""

import os
import sys
from pathlib import Path

MIN_PYTHON = (3, 8)

REQUIRED = {
    "numpy": "NumPy (vectorized arrays)",
    "pandas": "pandas (DataFrames)",
    "matplotlib": "matplotlib (visualization)",
    "ipykernel": "ipykernel (Jupyter kernel integration)",
}

BAR = "=" * 58


def header(title: str) -> None:
    print(BAR)
    print(f"  {title}")
    print(BAR)


def check_python() -> bool:
    version = sys.version_info
    label = f"{version.major}.{version.minor}.{version.micro}"
    print(f"[*] Python version: {label} ... ", end="")
    if version >= MIN_PYTHON:
        print("PASS")
        return True
    print(f"FAIL (require {MIN_PYTHON[0]}.{MIN_PYTHON[1]}+)")
    return False


def check_virtualenv() -> bool:
    """Warn if running against system Python instead of the project .venv."""
    in_venv = sys.prefix != getattr(sys, "base_prefix", sys.prefix)
    print(f"[*] Virtual environment active ... ", end="")
    if in_venv:
        print(f"PASS ({Path(sys.prefix).name})")
        return True
    print("WARNING (not in a venv -- packages may be installing system-wide)")
    return True  # warn, do not block


def check_dependencies() -> bool:
    missing = []
    for module, description in REQUIRED.items():
        print(f"[*] {description} ... ", end="")
        try:
            imported = __import__(module)
            print(f"PASS (v{getattr(imported, '__version__', 'unknown')})")
        except ImportError:
            print("FAIL")
            missing.append(module)

    if missing:
        print("\n[X] Missing dependencies. Run:")
        print(f"      pip install {' '.join(missing)}")
        print("    Or, preferred:")
        print("      pip install -r requirements.txt")
        return False
    return True


def check_numpy_broadcasting() -> bool:
    """Verify keepdims broadcasting -- the exact bug Exercise-level code hits."""
    import numpy as np

    print("    [*] NumPy broadcasting with keepdims ... ", end="")
    try:
        features = np.random.rand(100, 3)
        column_means = features.mean(axis=0, keepdims=True)
        assert column_means.shape == (1, 3), f"expected (1, 3), got {column_means.shape}"
        centered = features - column_means
        assert centered.shape == (100, 3), f"expected (100, 3), got {centered.shape}"
        assert np.allclose(centered.mean(axis=0), 0.0), "centering did not zero the column means"
        print("PASS")
        return True
    except AssertionError as exc:
        print(f"FAIL ({exc})")
        return False


def check_pandas_alignment() -> bool:
    """Verify pandas index alignment behaves as documented.

    This deliberately tests BOTH directions: a mismatched index must introduce
    NaN, and a reset index must not. Testing only the happy path would pass
    trivially and prove nothing.
    """
    import numpy as np
    import pandas as pd

    print("    [*] pandas index alignment semantics ... ", end="")
    try:
        df = pd.DataFrame(np.random.rand(100, 2), columns=["a", "b"])

        # Negative case: mismatched labels MUST introduce NaN.
        mismatched = pd.Series(np.random.rand(100), index=range(50, 150))
        df["mismatched"] = mismatched
        assert df["mismatched"].isnull().sum() > 0, (
            "expected NaN padding from mismatched index but got none -- "
            "pandas alignment semantics differ from what this project assumes"
        )

        # Positive case: reset index MUST align cleanly.
        clean = pd.Series(np.random.rand(100))
        df["clean"] = clean.reset_index(drop=True)
        assert df["clean"].isnull().sum() == 0, "reset index still introduced NaN"

        print("PASS")
        return True
    except AssertionError as exc:
        print(f"FAIL ({exc})")
        return False


def check_matplotlib_render() -> bool:
    """Confirm matplotlib can render and write a file to disk."""
    import matplotlib

    matplotlib.use("Agg")  # headless backend -- no display required
    import matplotlib.pyplot as plt
    import numpy as np

    print("    [*] matplotlib headless render and save ... ", end="")
    test_path = Path("_env_verify_test.png")
    try:
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(np.random.rand(50), label="verification trend")
        ax.set_title("L02 Environment Verification")
        ax.set_xlabel("Sample index")
        ax.set_ylabel("Value")
        ax.legend()
        ax.grid(True, alpha=0.3)
        fig.savefig(test_path, dpi=100, bbox_inches="tight")
        plt.close(fig)

        assert test_path.exists() and test_path.stat().st_size > 0, "figure file was not written"
        print("PASS")
        return True
    except Exception as exc:  # noqa: BLE001 -- surface any backend failure
        print(f"FAIL ({exc})")
        return False
    finally:
        if test_path.exists():
            os.remove(test_path)


def check_validator_importable() -> bool:
    """Confirm src/pipeline_validator.py imports from the repository root."""
    print("    [*] PipelineValidator import ... ", end="")
    repo_root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(repo_root))
    try:
        from src.pipeline_validator import PipelineValidator  # noqa: F401
        print("PASS")
        return True
    except Exception as exc:  # noqa: BLE001
        print(f"FAIL ({exc})")
        return False


def main() -> int:
    header("ITAI-1371 : L02 Local Environment Gate")

    if not check_python():
        print("\n[X] BLOCKED: Python version too old.")
        return 1

    check_virtualenv()

    if not check_dependencies():
        print("\n[X] BLOCKED: install dependencies and re-run.")
        return 1

    print("\n[*] Running functional checks ...")
    functional = [
        check_numpy_broadcasting(),
        check_pandas_alignment(),
        check_matplotlib_render(),
        check_validator_importable(),
    ]

    print()
    if not all(functional):
        print("[X] BLOCKED: one or more functional checks failed.")
        print("    Do not start the lab until this exits cleanly.")
        print(BAR)
        return 1

    print("[OK] Environment verified. You are cleared to open")
    print("     Module_02_Lab_Exercises.ipynb and bind the .venv kernel.")
    print(BAR)
    return 0


if __name__ == "__main__":
    sys.exit(main())
