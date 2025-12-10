from __future__ import annotations

"""Simple text-based menu system for PyDataUtils.

This module is intentionally small and beginner-friendly. It provides a
``run_menu`` function that can be executed either from a Python script
or from a Jupyter notebook cell.

The menu allows the user to:

1. Clean a single product name.
2. Clean a list of product names (entered manually).
3. Compute statistics on numbers using pure Python and NumPy.
4. Quit the program.

The goal is not to build a full CLI application, but to:

- Demonstrate **control flow** with ``if``/``elif``/``else`` and loops.
- Show how a menu can **call functions** from another module
  (``src.utilities``).
- Provide a slightly more interactive experience in the notebook.
"""

from typing import List

from .utilities import (
    clean_product_name,
    clean_product_names,
    compare_python_numpy_stats,
    format_comparison,
)


def _prompt(msg: str) -> str:
    """Wrapper around ``input`` for easier testing/patching.

    In a Jupyter notebook, this will display a text box in the cell
    output area.
    """

    return input(msg)


def _parse_numbers(raw: str) -> List[float]:
    """Parse a comma- or space-separated string of numbers into a list.

    Examples
    --------
    ``"1, 2, 3"`` -> ``[1.0, 2.0, 3.0]``

    ``"10 20 30"`` -> ``[10.0, 20.0, 30.0]``
    """

    # Replace commas with spaces, then split on whitespace
    pieces = raw.replace(",", " ").split()
    numbers: List[float] = []
    for p in pieces:
        if not p:
            continue
        try:
            numbers.append(float(p))
        except ValueError:
            raise ValueError(f"Could not convert {p!r} to a number") from None
    return numbers


def _menu_text() -> str:
    """Return the main menu text as a string."""

    return (
        "\nPyDataUtils Menu"\
        "\n================"\
        "\n1. Clean a single product name"\
        "\n2. Clean a list of product names"\
        "\n3. Compute statistics (Python vs NumPy)"\
        "\n4. Quit"\
        "\n\nEnter your choice (1-4): "
    )


def run_menu() -> None:
    """Run the interactive text-based menu.

    This function loops until the user chooses to quit. It performs
    basic error handling to keep the experience smooth for beginners.
    """

    while True:
        choice = _prompt(_menu_text()).strip()

        if choice == "1":
            # Clean a single product name
            raw = _prompt("\nEnter a product name to clean: ")
            cleaned = clean_product_name(raw)
            print(f"\nOriginal: {raw!r}")
            print(f"Cleaned : {cleaned!r}\n")

        elif choice == "2":
            # Clean a list of product names
            print("\nEnter product names separated by commas.")
            raw = _prompt("Names: ")
            # Split on commas, strip whitespace
            names = [part.strip() for part in raw.split(",") if part.strip()]
            cleaned_list = clean_product_names(names)
            print("\nCleaned product names:")
            for original, cleaned in zip(names, cleaned_list):
                print(f"- {original!r} -> {cleaned!r}")
            print()

        elif choice == "3":
            # Compute statistics
            print(
                "\nEnter numbers separated by commas or spaces "
                "(e.g. '1, 2, 3' or '1 2 3')."
            )
            raw = _prompt("Numbers: ")
            try:
                values = _parse_numbers(raw)
            except ValueError as exc:
                print(f"\nError: {exc}\n")
                continue

            if not values:
                print("\nNo numbers entered. Please try again.\n")
                continue

            comp = compare_python_numpy_stats(values)
            print("\n" + format_comparison(comp) + "\n")

        elif choice == "4":
            print("\nGoodbye!\n")
            break

        else:
            print("\nInvalid choice. Please enter a number between 1 and 4.\n")
