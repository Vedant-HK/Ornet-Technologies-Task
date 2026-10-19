# Task 2: SQL Database + Python Data Analysis


# Overview

This notebook analyzes an employee dataset using **Pandas** and **SQLite**. It demonstrates SQL queries, summary statistics, data-quality checks, duplicate detection, validation assertions, and a findings summary.

# Files

Keep these files together:

```text
Task2/
├── Task2.ipynb
├── employees.csv
└── README.md
```

The notebook looks for a file named `employees.csv` in the current folder or in common Google Colab locations. In Google Colab, it prompts you to upload the CSV if it cannot find the file.

> If your shared dataset is currently named `employees_shared.csv`, either rename it to `employees.csv` or update the filename in the notebook's `locate_employee_csv()` function.

# Requirements

- Python 3
- Pandas
- Jupyter Notebook or Google Colab
- SQLite support from Python's standard library (`sqlite3`)

In Google Colab, Pandas is normally preinstalled. If running locally, install Pandas and Jupyter if needed:

```bash
python -m pip install pandas notebook
```

No separate SQLite server is required. The notebook creates an **in-memory SQLite database**.

# How to run

1. Place `Task2.ipynb` and `employees.csv` together, or upload the CSV when prompted in Colab.
2. Open the notebook in Google Colab or Jupyter.
3. Run all cells from top to bottom.
4. Review the SQL results, Pandas summaries, data-quality tables, validation checks, and findings summary.

# Analysis performed

1. **Top five highest-paid employees** — SQL query ordered by salary, with employee ID used to break ties.
2. **Average salary by department** — SQL aggregation using `GROUP BY`.
3. **Data-quality checks** — records with missing salaries, missing ages, and invalid ages.
4. **Pandas analysis** — total records, unique employee IDs, average salary, and employee counts by department.
5. **Duplicate investigation** — repeated employee IDs and exact duplicate rows.
6. **Validation assertions** — checks expected dataset properties and selected query results.
7. **Findings summary** — prints the main statistics and data-quality counts.

# Dataset assumptions and data-quality rules

The supplied synthetic dataset is expected to contain 200 records and these intentional quality cases:

- 8 missing salaries
- 6 missing ages
- 3 negative salary values
- 3 invalid ages (negative, above 120, or fractional)
- 200 unique employee IDs
- No exact duplicate rows

The notebook treats employee IDs as identifiers. Missing values are reported rather than silently replaced.

# Salary handling

- Missing salaries are excluded from salary averages and rankings.
- Negative salaries are invalid and should also be excluded from salary averages, department averages, and highest-paid employee rankings.
- Do not replace missing salaries with zero.
- Employee counts should still include records with missing or invalid salary data, unless a separate, explicitly documented headcount rule is applied.

# Age handling

Ages are assumed to be whole numbers from 0 through 120. Missing ages are reported separately from invalid ages. Invalid values should be checked against the source rather than silently corrected.

# Duplicate handling

Repeated employee IDs and exact duplicate rows are flagged for investigation. The notebook does not automatically delete rows. Remove an exact duplicate only after confirming it is accidental; investigate conflicting records with the same employee ID before deciding which record is correct.

# Important consistency check

The validation and findings-summary cells exclude negative salaries from the valid overall average. Make sure the SQL queries use the same rule for consistent results:

```sql
WHERE salary IS NOT NULL
  AND salary >= 0
```

Use this condition in the top-five query. For department averages, use a filtered salary expression or filter invalid salary rows before grouping, while preserving department counts separately if you need counts of all employee records.

The notebook's expected-value assertions are specific to the supplied 200-row dataset. If the dataset changes, review the data-quality counts and update those expected values before rerunning the assertions.

# External libraries

- **Pandas** — CSV loading, data analysis, and result display.
- **SQLite (`sqlite3`)** — SQL queries using an in-memory database.
- **Pathlib** — locating the CSV file.
- **IPython display** — displaying tables in the notebook.

# Scope and limitations

This is a small assessment exercise using synthetic data. The results describe only the supplied dataset. No source CSV records are changed by creating the in-memory SQLite database; duplicate removal or correction is not performed automatically.
