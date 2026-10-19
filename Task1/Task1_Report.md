# Task 1 — Python Code Correction & Debugging

## Objective
Correct `unique_values()` so that it removes duplicate values while preserving the order of their first occurrences.

## Problem identified
The original statement `result.append(items)` appends the complete input iterable instead of the current loop value. The correction is `result.append(item)`.

## Implementation
- **Implementation file:** `Task1/task1_python_debugging.py`
- **Test file:** `Task1/test_task1.py`
- The function accepts an iterable and returns a list.
- Membership is checked against the values already collected, so order is preserved.
- The input is not modified.
- The implementation also supports unhashable values such as lists and accepts generators.

## Dependencies
Python 3.9 or newer; no third-party libraries. Tests use the standard-library `unittest` module.

## Verification
The submitted test suite covers duplicate removal, empty input, order preservation, non-mutation of the input, unhashable elements, and generator input. The six tests passed in the review run.

## Complexity and design decision
Worst-case time complexity is O(n²) because each new item may be compared with previously collected values. Additional space is O(n). This straightforward approach supports unhashable elements; a set-based approach may be faster for hashable-only inputs but would narrow the supported input types.

## Run
From `Task1/`:
```bash
python task1_python_debugging.py
python -m unittest -v test_task1
```
Expected example output: `[1, 2, 3]`.

## Assumptions and limitations
Elements must support equality comparisons. A non-iterable input raises `TypeError`. Equality behavior follows Python semantics.

## Suggested demonstration
Explain the incorrect append statement, run the example, then run the tests and explain why a set was not used.
