"""Defensive validation helpers for the ITAI-1371 L02 data pipeline.

Four checks, each guarding a specific silent-failure mode documented in
docs/tdd-assertion-guide.md:

    check_alignment    -- pandas index mismatch -> silent NaN padding
    check_broadcasting -- NumPy dimension squeeze -> wrong math, no error
    check_integrity    -- NaN / inf propagation -> destroyed gradients
    check_scale        -- failed normalization -> feature domination

Every method raises AssertionError with a diagnostic message on failure and
prints a PASS line on success. Failing loudly at the point of corruption is the
entire purpose; do not wrap these in try/except.

Usage
-----
    from src.pipeline_validator import PipelineValidator as PV

    PV.check_integrity(raw_features, name="Raw features")
    normalized = (features - col_means) / col_ranges
    PV.check_integrity(normalized, name="Normalized features")
    PV.check_scale(normalized)
"""

from __future__ import annotations  # keeps `X | Y` hints valid on Python 3.8/3.9

from typing import Union

import numpy as np
import pandas as pd

ArrayLike = Union[np.ndarray, pd.DataFrame, pd.Series]

__all__ = ["PipelineValidator"]


def _to_numeric_array(data: ArrayLike, name: str) -> np.ndarray:
    """Coerce a DataFrame, Series, or ndarray to a numeric NumPy array.

    Why this exists: ``DataFrame.values`` on a mixed-dtype frame returns an
    ``object`` array. ``np.isfinite()`` then raises a bare TypeError that says
    nothing about which column caused it. Coercing first turns an opaque crash
    into a message that names the problem.
    """
    if isinstance(data, (pd.DataFrame, pd.Series)):
        numeric = data.select_dtypes(include=[np.number]) if isinstance(data, pd.DataFrame) else data
        if isinstance(numeric, pd.DataFrame) and numeric.shape[1] != data.shape[1]:
            dropped = set(data.columns) - set(numeric.columns)
            raise AssertionError(
                f"[Integrity Fail] {name} contains non-numeric columns that cannot be "
                f"checked for finiteness: {sorted(dropped)}. Select numeric columns "
                f"explicitly before validating."
            )
        array = numeric.to_numpy()
    else:
        array = np.asarray(data)

    if not np.issubdtype(array.dtype, np.number):
        raise AssertionError(
            f"[Integrity Fail] {name} has non-numeric dtype '{array.dtype}'. "
            f"Finiteness checks require a numeric array."
        )
    return array


class PipelineValidator:
    """Static assertion helpers. No state; call directly on the class."""

    # ------------------------------------------------------------------
    # 1. Index alignment -- the silent killer of pandas assignments
    # ------------------------------------------------------------------
    @staticmethod
    def check_alignment(
        df: pd.DataFrame,
        series: pd.Series,
        label: str = "Feature",
    ) -> None:
        """Assert that a Series index matches the target DataFrame index exactly.

        Pandas aligns on index labels, not row positions. A filtered Series keeps
        its original labels; assigning it to a frame with a different index pads
        the mismatches with NaN and raises nothing. Length equality is not
        sufficient -- indices 0-99 and 1-100 are the same length and still corrupt.
        """
        assert isinstance(df, pd.DataFrame), f"check_alignment expects a DataFrame, got {type(df).__name__}"
        assert isinstance(series, pd.Series), f"check_alignment expects a Series, got {type(series).__name__}"

        assert df.index.equals(series.index), (
            f"[Alignment Fail] {label} index does not match the target DataFrame index.\n"
            f"  DataFrame index: len={len(df.index)}, first={list(df.index[:3])}, last={list(df.index[-3:])}\n"
            f"  Series index:    len={len(series.index)}, first={list(series.index[:3])}, last={list(series.index[-3:])}\n"
            f"  Fix: .reset_index(drop=True) on both, or use an explicit join."
        )
        print(f"[Alignment PASS] {label} index matches exactly (length {len(df.index)}).")

    # ------------------------------------------------------------------
    # 2. Broadcasting shape -- prevents silently wrong matrix math
    # ------------------------------------------------------------------
    @staticmethod
    def check_broadcasting(
        matrix: np.ndarray,
        vector: np.ndarray,
        axis: int = 0,
    ) -> None:
        """Assert a vector retains explicit 2D shape for broadcasting over a matrix.

        ``matrix.mean(axis=0)`` squeezes to shape ``(cols,)``. Subtracting that
        from a ``(rows, cols)`` matrix may still run -- and produce wrong numbers.
        Use ``keepdims=True`` to retain ``(1, cols)``.

        axis=0 -> column-wise statistic, expected shape (1, n_cols)
        axis=1 -> row-wise statistic,    expected shape (n_rows, 1)
        """
        matrix = np.asarray(matrix)
        vector = np.asarray(vector)

        assert matrix.ndim == 2, f"[Broadcasting Fail] Matrix must be 2D, got {matrix.ndim}D with shape {matrix.shape}."
        assert axis in (0, 1), f"[Broadcasting Fail] axis must be 0 or 1, got {axis}."

        expected = (1, matrix.shape[1]) if axis == 0 else (matrix.shape[0], 1)
        assert vector.shape == expected, (
            f"[Broadcasting Fail] Expected vector shape {expected} for axis={axis}, "
            f"got {vector.shape}.\n"
            f"  Matrix shape: {matrix.shape}\n"
            f"  Fix: pass keepdims=True to the reduction, or reshape with .reshape(-1, 1) / [np.newaxis, :]."
        )
        print(f"[Broadcasting PASS] Vector {vector.shape} broadcasts safely over matrix {matrix.shape}.")

    # ------------------------------------------------------------------
    # 3. Numerical integrity -- catches NaN and inf together
    # ------------------------------------------------------------------
    @staticmethod
    def check_integrity(data: ArrayLike, name: str = "Dataset") -> None:
        """Assert no NaN, +inf, or -inf values exist.

        ``np.isfinite().all()`` is used rather than ``.isna().sum() == 0``
        because the latter misses infinities, which destroy gradients just as
        thoroughly as NaN.
        """
        array = _to_numeric_array(data, name)
        finite_mask = np.isfinite(array)

        if not finite_mask.all():
            nan_count = int(np.isnan(array).sum())
            inf_count = int(np.isinf(array).sum())
            bad_positions = np.argwhere(~finite_mask)[:5].tolist()
            raise AssertionError(
                f"[Integrity Fail] {name} contains invalid values.\n"
                f"  NaN count: {nan_count}\n"
                f"  Inf count: {inf_count}\n"
                f"  First bad positions: {bad_positions}\n"
                f"  Fix: impute, clip, or drop before this step -- do not pass this downstream."
            )
        print(f"[Integrity PASS] {name} is clean: no NaN, no inf ({array.size} values checked).")

    # ------------------------------------------------------------------
    # 4. Scale boundary -- proves normalization actually normalized
    # ------------------------------------------------------------------
    @staticmethod
    def check_scale(
        data: ArrayLike,
        min_val: float = 0.0,
        max_val: float = 1.0,
        name: str = "Scaled data",
    ) -> None:
        """Assert all values lie within the expected normalization bounds.

        Run this AFTER check_integrity -- min/max on an array containing NaN
        returns NaN, and every comparison against NaN is False, so this check
        would fail with a misleading message.
        """
        array = _to_numeric_array(data, name)
        actual_min = float(array.min())
        actual_max = float(array.max())

        assert actual_min >= min_val and actual_max <= max_val, (
            f"[Scale Fail] {name} exceeds expected bounds.\n"
            f"  Expected: [{min_val}, {max_val}]\n"
            f"  Actual:   [{actual_min:.6f}, {actual_max:.6f}]\n"
            f"  Fix: check the denominator in your min-max formula -- a zero-range "
            f"column or a mismatched axis is the usual cause."
        )
        print(f"[Scale PASS] {name} within [{actual_min:.4f}, {actual_max:.4f}].")
