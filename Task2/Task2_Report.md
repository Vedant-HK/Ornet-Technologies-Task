# Task 2 — SQL Database + Python Data Analysis

## Objective
Query an employee dataset using SQL and produce descriptive statistics and data-quality checks using Python/Pandas.

## Files
- `Task2/Task2.ipynb` — notebook containing data loading, SQL, analysis, validation, and findings.
- `Task2/employees.csv` — supplied dataset.
- `Task2/README.md` — setup and assumptions.

## Method
1. Load the CSV with Pandas and validate the required columns: `employee_id`, `name`, `department`, `salary`, and `age`.
2. Convert numeric fields explicitly; invalid numeric text is treated as missing for review.
3. Load the DataFrame into an in-memory SQLite database.
4. Run SQL for the top five salaries, average salary by department, missing salaries, missing ages, and invalid ages.
5. Use Pandas for employee-record counts, unique employee IDs, average salary, department counts, and duplicate checks.
6. Run assertions against expected properties of the supplied synthetic dataset and print a findings summary.

## Libraries
- Pandas — CSV loading, analysis, and tabular output.
- `sqlite3` — in-memory SQL database (Python standard library).
- `pathlib` — file path resolution.
- IPython display — notebook table display.

## Dataset assumptions documented in the project
The notebook README expects 200 records, 200 unique employee IDs, 8 missing salaries, 6 missing ages, 3 negative salaries, 3 invalid ages, and no exact duplicate rows. These expected values are specific to the bundled dataset.

## Data-quality policy
- Report missing salaries and ages; do not silently replace missing values with zero.
- Treat ages as valid only when they are whole numbers between 0 and 120.
- Flag repeated employee IDs and exact duplicate rows for investigation rather than deleting records automatically.
- Salary-based calculations should exclude missing and negative salaries. Headcount should continue to count employee records unless a separate rule is explicitly stated.

## Important verification note
The current notebook has inconsistent salary filters: the top-five SQL query excludes missing salaries but does not exclude negative salaries, the department-average query also does not exclude negative salaries, and the overall-average cell uses all non-missing salaries. Later validation and findings-summary cells exclude negative salaries. Before submission, apply the same rule to all salary calculations, for example `salary IS NOT NULL AND salary >= 0`, and rerun the notebook from a fresh runtime.

The notebook README also documents an expected duplicate-free dataset; confirm that the actual duplicate-check output and assertions agree before finalizing the findings.

## Run
Open `Task2/Task2.ipynb` in Google Colab or Jupyter, ensure `employees.csv` is available beside the notebook (or upload it in Colab), then run all cells from top to bottom.

## Deliverables and limitations
The deliverable is a notebook, not a separate `.py` script. The results describe only the bundled synthetic dataset and do not automatically repair or delete source records.

## Suggested demonstration
Show the schema validation, SQL table creation, each SQL result, the Pandas summary, data-quality checks, and the final assertions. Explain why missing values are reported rather than replaced and why duplicate records require investigation.
