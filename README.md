# ORNET Technologies — AI Developer Practical Assessment

This package documents the four tasks in the submitted assessment ZIP. The official assessment asks for all four tasks, readable Python/SQL, tests and error handling, documented assumptions and libraries, AI-assistance disclosure, a README, and readiness to explain the technical decisions.

## Task deliverables
- **Task 1:** Python function correction, separate `unittest` suite, and README.
- **Task 2:** Jupyter/Colab notebook, employee CSV, SQL queries, Pandas summaries, data-quality checks, and README.
- **Task 3:** Written ML/LLM conceptual debugging answers in README.
- **Task 4:** Python tool functions, CLI/Streamlit interfaces, employee CSV, offline tests, requirements, and README.

## How to run
Run each task from its own folder. See the corresponding task README and the task-specific reports in this documentation bundle.

## Review findings to resolve before submission
1. **Task 2:** Align SQL and Pandas salary calculations so missing and negative salaries are consistently excluded from salary averages and rankings. Confirm duplicate-check output matches the documented dataset assumptions, then rerun the notebook top-to-bottom.
2. **Task 4:** Remove `.env` and any real credentials from the submission. Remove the hard-coded credential from `agent.py`; read the API key from an environment variable or secrets store. Rotate the credential if it is real. Test Gemini mode separately from offline unit tests.
3. Remove generated `__pycache__` and unnecessary `.dist` artifacts from the final ZIP.
4. Verify every README command and expected output on the final cleaned package.

## AI assistance disclosure
AI coding assistance was used to help draft/review code and documentation in parts of this submission.