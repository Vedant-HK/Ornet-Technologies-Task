# Task 1 — Python Code Correction & Debugging

# Overview

This task corrects a Python function that removes duplicate values from an iterable while preserving the original order of first occurrences.

# Project structure

```text
Task1/
├── task1_python_debugging.py
├── test_task1.py
└── README.md
```

- `task1_python_debugging.py` contains the `unique_values()` implementation.
- `test_task1.py` contains independent automated tests using Python's built-in `unittest` framework.

# Requirements

- Python 3.9 or newer (the implementation uses built-in generic type annotations such as `list[T]`).
- No third-party packages are required.

# How to run

Open a terminal in the `Task1` directory.

# 1. Run the example

```bash
python task1_python_debugging.py
```

Expected output:

```text
[1, 2, 3]
```

# 2. Run the test suite

```bash
python -m unittest -v test_task1
```

The terminal reports each test case individually with `ok` for a passing test and displays details if a test fails.

# Test coverage

The test suite verifies that the function:

1. Removes duplicate values.
2. Handles an empty list.
3. Preserves the original order of first occurrences.
4. Does not modify the input list.
5. Supports unhashable elements such as nested lists.
6. Accepts a generator as input.

# Bug explanation

The original function used:

```python
result.append(items)
```

This appends the entire input iterable instead of the current item. The corrected statement is:

```python
result.append(item)
```

As a result, the function now collects each first-seen value rather than appending the input container.

# Design decisions

- The implementation and tests are kept in separate files.
- The function uses type hints and a docstring to make its interface clear.
- It preserves order and does not mutate the input.
- It does not use a set, so it can also handle unhashable values such as lists.

# Complexity

For `n` input elements, the implementation has **O(n²) worst-case time complexity**, because each item may be compared with values already collected. The result uses **O(n) additional space** in the worst case.

This trade-off keeps the implementation straightforward and supports unhashable elements. For inputs restricted to hashable values, a set-based membership check could improve expected runtime to O(n).

# Assumptions and limitations

- Elements are expected to support equality comparisons.
- The function accepts any iterable; a non-iterable input raises Python's `TypeError`.
- Equality behavior follows Python's normal comparison semantics.

