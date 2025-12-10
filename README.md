# PyDataUtils

PyDataUtils
===========

A **beginner-friendly Python data science mini-project** that demonstrates how to:

- Build and use **utility functions** for lists, strings, and NumPy arrays
- Compare **pure Python** implementations with **NumPy-based** implementations
- Organize a small data science project with a clean, portfolio-ready structure
- Work interactively in a **Jupyter Notebook** while keeping reusable code in a `src/` module

This project focuses on a simple but realistic scenario: working with a list of product names and numeric data, cleaning the text, and computing basic statistics using both core Python and NumPy.

---

## Project Structure

```text
PyDataUtils/
├─ README.md
├─ requirements.txt
├─ environment.yml
├─ .gitignore
├─ data/
│  └─ sample_products.csv
├─ notebooks/
│  └─ PyDataUtils.ipynb
└─ src/
   ├─ __init__.py
   ├─ utilities.py
   └─ menu.py
```

### Key Components

- **`notebooks/PyDataUtils.ipynb`**  
  Main notebook with:
  - Product name cleaner demonstrations
  - Statistics calculations (pure Python & NumPy)
  - A simple text-based **menu system** driving the utilities

- **`src/utilities.py`**  
  Reusable utility functions for:
  - **String cleaning** (product names)
  - **List utilities** (e.g., flattening, deduplication)
  - **Statistics** implemented with pure Python and NumPy

- **`src/menu.py`**  
  A **text-based menu** that:
  - Presents options in the notebook or terminal
  - Calls the appropriate functions in `utilities.py`

- **`data/sample_products.csv`**  
  Simple CSV file with product names containing extra spaces, mixed case, and special characters to practice cleaning.

---

## Installation

You can set up the project using either **pip** or **conda**.

### Option 1: Using `pip`

1. (Optional but recommended) Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS / Linux
   source .venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Launch Jupyter Notebook:

   ```bash
   jupyter notebook
   ```

4. Open `notebooks/PyDataUtils.ipynb` from the Jupyter interface.

### Option 2: Using `conda`

1. Create the environment from `environment.yml`:

   ```bash
   conda env create -f environment.yml
   ```

2. Activate the environment:

   ```bash
   conda activate pydatautils
   ```

3. Launch Jupyter Notebook:

   ```bash
   jupyter notebook
   ```

4. Open `notebooks/PyDataUtils.ipynb`.

---

## Usage Overview

In the notebook, you will:

1. **Import utilities** from the `src` package:

   ```python
   from src.utilities import (
       clean_product_name,
       clean_product_names,
       python_stats,
       numpy_stats,
       compare_python_numpy_stats,
   )

   from src.menu import run_menu
   ```

2. **Load sample product data** from the CSV file:

   ```python
   import pandas as pd

   df = pd.read_csv("../data/sample_products.csv")
   df.head()
   ```

3. **Clean product names**:

   ```python
   cleaned = clean_product_names(df["product_name"])
   cleaned[:5]
   ```

4. **Compute statistics** on numeric columns:

   ```python
   prices = df["price"].tolist()
   python_stats(prices)
   numpy_stats(prices)
   compare_python_numpy_stats(prices)
   ```

5. **Use the interactive menu**:

   ```python
   # This will run a simple text menu inside the notebook cell output
   run_menu()
   ```

---

## Concepts Demonstrated

This small project touches on many **fundamental Python and data science concepts**:

- **Core Python**
  - Variables and basic data types
  - Control flow: `if`, `elif`, `else`, `for`, `while`
  - Functions and parameters
  - Lists, dictionaries, list comprehensions
  - String methods and simple regular expressions

- **NumPy**
  - Creating arrays from lists
  - Vectorized operations
  - Basic statistics with NumPy
  - Comparing performance vs pure Python

- **Project structure & workflow**
  - Separating code into `src/` modules
  - Keeping data under `data/`
  - Using a single main notebook for exploration
  - Requirements and environment files for reproducibility

---

## Example: Product Name Cleaning

Given messy names like:

```text
"  Super-Deluxe Toaster!!! "
"BASIC kettle (white)"
"   Mega_MIXER 3000   "
"coffee-maker#1"
```

The `clean_product_name` function will:

- Strip leading/trailing spaces
- Convert to lowercase
- Replace non-alphanumeric characters with a single space
- Collapse multiple spaces into one

Resulting in:

```text
"super deluxe toaster"
"basic kettle white"
"mega mixer 3000"
"coffee maker 1"
```

---

## Example: Pure Python vs NumPy Stats

Using a Python list of numbers, e.g.:

```python
values = [10, 20, 30, 40, 50]
```

You can compute statistics in **pure Python**:

```python
python_stats(values)
```

and with **NumPy**:

```python
numpy_stats(values)
```

`compare_python_numpy_stats(values)` computes both and checks that the results are consistent, while also measuring basic execution time.

---

## Extending the Project

Ideas for improvements and practice:

- Add more string utilities (e.g. slug generation, simple tokenization)
- Implement additional statistics (median, variance, quantiles)
- Add basic plotting examples with Matplotlib or pandas
- Enhance the menu system with new options and better error handling

---

## License

This project is intended as a learning resource. You may reuse and adapt the code freely for personal and educational purposes.
