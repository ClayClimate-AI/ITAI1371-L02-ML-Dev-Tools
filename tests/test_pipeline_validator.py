"""Regression tests for PipelineValidator.

The point of these tests is not to prove the happy path works. It is to prove
each check FAILS on the exact silent-corruption case it was written to catch.

An assertion helper that passes on bad input is worse than no helper: it
manufactures confidence. Every test below feeds known-bad data and asserts that
an AssertionError is raised.

Run:  pytest tests/ -v
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.pipeline_validator import PipelineValidator as PV  # noqa: E402


# ----------------------------------------------------------------------
# 1. check_alignment
# ----------------------------------------------------------------------

def test_alignment_passes_on_matching_index():
    df = pd.DataFrame({"a": [1.0, 2.0, 3.0]})
    series = pd.Series([4.0, 5.0, 6.0])
    PV.check_alignment(df, series, label="Matching")


def test_alignment_fails_on_filtered_index():
    """The real-world case: a filtered Series keeps its original labels."""
    df = pd.DataFrame({"a": [1.0, 2.0, 3.0]})
    filtered = pd.Series([10.0, 20.0, 30.0], index=[0, 2, 5])
    with pytest.raises(AssertionError, match="Alignment Fail"):
        PV.check_alignment(df, filtered, label="Filtered")


def test_alignment_fails_on_same_length_shifted_index():
    """Equal length, different labels. A len() check would miss this entirely."""
    df = pd.DataFrame({"a": [1.0, 2.0, 3.0]})                # index 0,1,2
    shifted = pd.Series([1.0, 2.0, 3.0], index=[1, 2, 3])    # index 1,2,3
    with pytest.raises(AssertionError, match="Alignment Fail"):
        PV.check_alignment(df, shifted, label="Shifted")


# ----------------------------------------------------------------------
# 2. check_broadcasting
# ----------------------------------------------------------------------

def test_broadcasting_passes_with_keepdims():
    matrix = np.random.rand(100, 4)
    means = matrix.mean(axis=0, keepdims=True)   # shape (1, 4)
    PV.check_broadcasting(matrix, means, axis=0)


def test_broadcasting_fails_on_squeezed_vector():
    """The classic bug: axis=0 without keepdims squeezes (1,4) down to (4,)."""
    matrix = np.random.rand(100, 4)
    squeezed = matrix.mean(axis=0)               # shape (4,) -- wrong
    with pytest.raises(AssertionError, match="Broadcasting Fail"):
        PV.check_broadcasting(matrix, squeezed, axis=0)


def test_broadcasting_fails_on_wrong_axis_orientation():
    matrix = np.random.rand(100, 4)
    row_means = matrix.mean(axis=1, keepdims=True)   # shape (100, 1)
    with pytest.raises(AssertionError, match="Broadcasting Fail"):
        PV.check_broadcasting(matrix, row_means, axis=0)  # declared wrong axis


def test_broadcasting_fails_on_1d_matrix():
    with pytest.raises(AssertionError, match="must be 2D"):
        PV.check_broadcasting(np.arange(10), np.array([[1.0]]), axis=0)


# ----------------------------------------------------------------------
# 3. check_integrity
# ----------------------------------------------------------------------

def test_integrity_passes_on_clean_array():
    PV.check_integrity(np.random.rand(50, 3), name="Clean")


def test_integrity_fails_on_nan():
    data = np.random.rand(50, 3)
    data[7, 1] = np.nan
    with pytest.raises(AssertionError, match="Integrity Fail"):
        PV.check_integrity(data, name="NaN injected")


def test_integrity_fails_on_positive_infinity():
    """np.isfinite catches inf; df.isna() would not. This is why we use isfinite."""
    data = np.random.rand(50, 3)
    data[3, 2] = np.inf
    with pytest.raises(AssertionError, match="Integrity Fail"):
        PV.check_integrity(data, name="Inf injected")


def test_integrity_fails_on_negative_infinity():
    data = np.random.rand(50, 3)
    data[10, 0] = -np.inf
    with pytest.raises(AssertionError, match="Integrity Fail"):
        PV.check_integrity(data, name="NegInf injected")


def test_integrity_reports_non_numeric_columns_clearly():
    """Mixed dtypes must produce a named diagnostic, not an opaque TypeError."""
    df = pd.DataFrame({"num": [1.0, 2.0], "label": ["setosa", "virginica"]})
    with pytest.raises(AssertionError, match="non-numeric columns"):
        PV.check_integrity(df, name="Mixed frame")


def test_integrity_accepts_numeric_dataframe():
    df = pd.DataFrame({"a": [1.0, 2.0], "b": [3.0, 4.0]})
    PV.check_integrity(df, name="Numeric frame")


# ----------------------------------------------------------------------
# 4. check_scale
# ----------------------------------------------------------------------

def test_scale_passes_on_normalized_data():
    PV.check_scale(np.linspace(0.0, 1.0, 100), name="Linspace")


def test_scale_fails_on_unnormalized_data():
    with pytest.raises(AssertionError, match="Scale Fail"):
        PV.check_scale(np.array([0.0, 0.5, 42.0]), name="Unscaled")


def test_scale_fails_on_negative_values():
    with pytest.raises(AssertionError, match="Scale Fail"):
        PV.check_scale(np.array([-0.3, 0.5, 0.9]), name="Negative")


def test_scale_boundaries_are_inclusive():
    """Exactly 0.0 and exactly 1.0 must pass -- min-max scaling produces both."""
    PV.check_scale(np.array([0.0, 0.5, 1.0]), name="Boundary")


def test_scale_accepts_custom_bounds():
    """Standardized data lives roughly in [-3, 3], not [0, 1]."""
    PV.check_scale(np.array([-2.5, 0.0, 2.9]), min_val=-3.0, max_val=3.0, name="Z-scored")
