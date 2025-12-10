from __future__ import annotations

"""Utility functions for the PyDataUtils project.

This module is intentionally **beginner-friendly** and aims to
illustrate clear, well-documented Python code along with basic NumPy
usage. The functions here are designed to be imported and used within
the main Jupyter notebook.

Topics covered:

- Simple **string cleaning** functions (focused on product names)
- Utility helpers for working with **lists**
- Basic **statistics** implemented in both pure Python and NumPy
- A helper to **compare** the two implementations

The goal is clarity, not maximum performance.
"""

from dataclasses import dataclass
import re
import time
from typing import Iterable, List, Sequence, Tuple, Dict, Any, Optional

import numpy as np


# ---------------------------------------------------------------------------
# String utilities
# ---------------------------------------------------------------------------

_clean_pattern = re.compile(r"[^a-z0-9]+")


def clean_product_name(name: str) -> str:
    """Clean a single product name.

    Steps:

    1. Convert to string (in case the value is not already a string).
    2. Strip leading and trailing whitespace.
    3. Convert to lowercase.
    4. Replace any **non-alphanumeric characters** with a single space.
    5. Collapse multiple spaces into a single space.

    Parameters
    ----------
    name:
        The original product name (any object; will be converted to ``str``).

    Returns
    -------
    str
        The cleaned product name.
    """

    # Convert to string in a safe way
    text = str(name)

    # Step 1: strip whitespace
    text = text.strip()

    # Step 2: lowercase
    text = text.lower()

    # Step 3: replace non-alphanumeric characters with a space
    text = _clean_pattern.sub(" ", text)

    # Step 4: collapse multiple spaces into a single space
    text = re.sub(r"\s+", " ", text)

    # Final strip to remove any leftover leading/trailing space
    return text.strip()


def clean_product_names(names: Iterable[Any]) -> List[str]:
    """Clean a sequence of product names.

    This simply applies :func:`clean_product_name` to every element in
    the input iterable and returns a new list of cleaned strings.

    Parameters
    ----------
    names:
        Any iterable of values that can be converted to strings.

    Returns
    -------
    list of str
        Cleaned product names.
    """

    return [clean_product_name(name) for name in names]


# ---------------------------------------------------------------------------
# List utilities
# ---------------------------------------------------------------------------


def flatten_list(nested: Iterable[Iterable[Any]]) -> List[Any]:
    """Flatten a list (or any iterable) of iterables into a single list.

    This function performs a *simple one-level flattening*. It does **not**
    recursively flatten arbitrarily deeply nested structures; that would be
    more advanced than needed for this project.

    Examples
    --------
    >>> flatten_list([[1, 2], [3, 4]])
    [1, 2, 3, 4]

    Parameters
    ----------
    nested:
        Iterable of iterables, e.g. ``list`` of ``list``.

    Returns
    -------
    list
        A flat list containing all elements of the nested input.
    """

    flat: List[Any] = []
    for sub in nested:
        for item in sub:
            flat.append(item)
    return flat


def unique_preserve_order(items: Iterable[Any]) -> List[Any]:
    """Return unique items from *items* while preserving first-seen order.

    Parameters
    ----------
    items:
        Any iterable.

    Returns
    -------
    list
        A list of unique items in the order they first appeared.
    """

    seen = set()
    result: List[Any] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


# ---------------------------------------------------------------------------
# Statistics utilities (pure Python)
# ---------------------------------------------------------------------------


def _validate_numeric_sequence(values: Sequence[float]) -> None:
    """Basic validation that *values* looks like a numeric sequence.

    This is intentionally minimal. It checks that:

    - ``values`` is not empty
    - Every element can be converted to ``float``

    Raises
    ------
    ValueError
        If the sequence is empty or if an element cannot be converted to
        a float.
    """

    if not values:
        raise ValueError("values must be a non-empty sequence")

    # Attempt float conversion; fail fast on error
    for v in values:
        try:
            float(v)
        except (TypeError, ValueError) as exc:  # pragma: no cover - defensive
            raise ValueError(f"Non-numeric value encountered: {v!r}") from exc


@dataclass
class StatsResult:
    """Container for basic descriptive statistics.

    Attributes
    ----------
    count:
        Number of observations.
    mean:
        Arithmetic mean of the values.
    minimum:
        Smallest value.
    maximum:
        Largest value.
    total:
        Sum of all values.
    impl:
        Implementation used (e.g. ``"python"`` or ``"numpy"``).
    """

    count: int
    mean: float
    minimum: float
    maximum: float
    total: float
    impl: str


def python_stats(values: Sequence[float]) -> StatsResult:
    """Compute basic statistics using **pure Python** loops.

    The function calculates:

    - count (number of elements)
    - sum (total)
    - mean
    - minimum
    - maximum

    Parameters
    ----------
    values:
        A non-empty sequence of numeric values.

    Returns
    -------
    StatsResult
        A dataclass instance with the computed statistics.
    """

    _validate_numeric_sequence(values)

    # Initialize with the first element
    iterator = iter(values)
    first = float(next(iterator))

    count = 1
    total = first
    minimum = first
    maximum = first

    # Loop over remaining values
    for v in iterator:
        x = float(v)
        count += 1
        total += x
        if x < minimum:
            minimum = x
        if x > maximum:
            maximum = x

    mean = total / count

    return StatsResult(
        count=count,
        mean=mean,
        minimum=minimum,
        maximum=maximum,
        total=total,
        impl="python",
    )


# ---------------------------------------------------------------------------
# Statistics utilities (NumPy)
# ---------------------------------------------------------------------------


def numpy_stats(values: Sequence[float]) -> StatsResult:
    """Compute basic statistics using **NumPy**.

    This converts the input sequence to a NumPy array of ``float64`` and
    then uses NumPy's vectorized functions to compute:

    - count
    - sum (total)
    - mean
    - minimum
    - maximum

    Parameters
    ----------
    values:
        A non-empty sequence of numeric values.

    Returns
    -------
    StatsResult
        A dataclass instance with the computed statistics.
    """

    _validate_numeric_sequence(values)

    arr = np.asarray(values, dtype="float64")

    count = int(arr.size)
    total = float(arr.sum())
    mean = float(arr.mean())
    minimum = float(arr.min())
    maximum = float(arr.max())

    return StatsResult(
        count=count,
        mean=mean,
        minimum=minimum,
        maximum=maximum,
        total=total,
        impl="numpy",
    )


# ---------------------------------------------------------------------------
# Comparison helper
# ---------------------------------------------------------------------------

@dataclass
class ComparisonResult:
    """Compare pure Python statistics with NumPy statistics.

    Attributes
    ----------
    python:
        :class:`StatsResult` computed by :func:`python_stats`.
    numpy:
        :class:`StatsResult` computed by :func:`numpy_stats`.
    are_equal:
        Boolean indicating whether the results match (within a small
        tolerance for floating-point comparisons).
    python_time:
        Execution time in seconds for the pure Python implementation.
    numpy_time:
        Execution time in seconds for the NumPy implementation.
    """

    python: StatsResult
    numpy: StatsResult
    are_equal: bool
    python_time: float
    numpy_time: float


def _stats_almost_equal(a: StatsResult, b: StatsResult, tol: float = 1e-9) -> bool:
    """Return True if two StatsResult objects are almost equal.

    The ``count`` field must match exactly, while floating-point fields
    are compared within the given absolute tolerance.
    """

    if a.count != b.count:
        return False

    def close(x: float, y: float) -> bool:
        return abs(x - y) <= tol

    return (
        close(a.mean, b.mean)
        and close(a.minimum, b.minimum)
        and close(a.maximum, b.maximum)
        and close(a.total, b.total)
    )


def compare_python_numpy_stats(values: Sequence[float]) -> ComparisonResult:
    """Compute and compare statistics using both Python and NumPy.

    This helper is useful in the notebook for **demonstrating** that both
    implementations produce (almost) the same results, and for showing a
    very basic timing comparison.

    Parameters
    ----------
    values:
        Sequence of numeric values.

    Returns
    -------
    ComparisonResult
        Dataclass containing both results and timing information.
    """

    start_py = time.perf_counter()
    py_result = python_stats(values)
    end_py = time.perf_counter()

    start_np = time.perf_counter()
    np_result = numpy_stats(values)
    end_np = time.perf_counter()

    are_equal = _stats_almost_equal(py_result, np_result)

    return ComparisonResult(
        python=py_result,
        numpy=np_result,
        are_equal=are_equal,
        python_time=end_py - start_py,
        numpy_time=end_np - start_np,
    )


# ---------------------------------------------------------------------------
# Simple helper for pretty-printing stats (useful in the notebook or menu)
# ---------------------------------------------------------------------------


def format_stats(result: StatsResult) -> str:
    """Return a nicely formatted multi-line string for a StatsResult.

    Parameters
    ----------
    result:
        Statistics result to format.

    Returns
    -------
    str
        Human-readable, multi-line description of the statistics.
    """

    return (
        f"Implementation: {result.impl}\n"
        f"Count         : {result.count}\n"
        f"Total         : {result.total:.6g}\n"
        f"Mean          : {result.mean:.6g}\n"
        f"Min           : {result.minimum:.6g}\n"
        f"Max           : {result.maximum:.6g}"
    )


def format_comparison(comp: ComparisonResult) -> str:
    """Return a formatted report comparing Python and NumPy statistics.

    Parameters
    ----------
    comp:
        ComparisonResult instance.

    Returns
    -------
    str
        Multi-line comparison report.
    """

    lines = [
        "=== Python implementation ===",
        format_stats(comp.python),
        "",
        "=== NumPy implementation ===",
        format_stats(comp.numpy),
        "",
        f"Results match (within tolerance): {comp.are_equal}",
        f"Python time: {comp.python_time:.6f} s",
        f"NumPy time : {comp.numpy_time:.6f} s",
    ]
    return "\n".join(lines)
