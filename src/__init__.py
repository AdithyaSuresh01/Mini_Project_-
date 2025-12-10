"""PyDataUtils src package.

This package contains simple, beginner-friendly utility functions for
working with:

- Lists and basic Python data structures
- String cleaning and normalization (focused on product names)
- Numeric statistics implemented in both pure Python and NumPy
- A small text-based menu wrapper for interactive exploration

The main entry point for exploration is the Jupyter notebook under
``notebooks/PyDataUtils.ipynb``. Typical usage in the notebook:

.. code-block:: python

    from src.utilities import (
        clean_product_name,
        clean_product_names,
        python_stats,
        numpy_stats,
        compare_python_numpy_stats,
    )

    from src.menu import run_menu

"""

from .utilities import (
    clean_product_name,
    clean_product_names,
    flatten_list,
    unique_preserve_order,
    python_stats,
    numpy_stats,
    compare_python_numpy_stats,
)

from .menu import run_menu

__all__ = [
    "clean_product_name",
    "clean_product_names",
    "flatten_list",
    "unique_preserve_order",
    "python_stats",
    "numpy_stats",
    "compare_python_numpy_stats",
    "run_menu",
]
