# Task 4 — Mini AI Data Assistant Agent

## Objective
Build an assistant that accepts natural-language questions about an employee dataset, maps requests to tools, performs calculations deterministically in Python, and returns readable answers.

## Files and responsibilities
- `Task4/agent.py` — intent representation/parsing, dispatch, answer formatting, and CLI entry point.
- `Task4/employee_tools.py` — data loading, validation, and employee/salary calculations.
- `Task4/streamlit_app.py` — browser-based chat interface and mode selection.
- `Task4/data/employees.csv` — bundled employee dataset.
- `Task4/tests/test_agent.py` — offline automated tests.
- `Task4/requirements.txt` — external dependencies.
- `Task4/README.md` — setup, operation, assumptions, and troubleshooting.

## Tools and behavior
- Employee count by department.
- Average salary.
- Highest-paid employee lookup.
- Proposed salary increase by department.
- Unsupported request handling and validation for department names and percentages.
- Salary calculations exclude missing and negative salary values.
- Proposed increases are calculations only; source records are not modified.
- Department matching is case-insensitive.

## Architecture
In Gemini mode, the LLM produces a constrained intent describing the requested tool and relevant arguments. The application validates and dispatches that intent to Python functions. Python—not the LLM—calculates counts and salary values. An offline parser supports demonstrations and unit tests without an API call; it is explicitly a limited demo path, not a replacement for the LLM requirement.

## Dependencies
- Pandas — employee CSV handling and calculations.
- `google-genai` — Gemini intent parsing.
- Streamlit — web interface.
- `python-dotenv` — local environment-variable loading.
- Python standard library — CLI, validation, JSON parsing, and `unittest`.

## Verification
The submitted offline test suite contains 17 tests and passed in the review run. These tests do not call the external Gemini API; therefore, passing unit tests alone does not establish that live LLM mode works. Perform a separate end-to-end test with a valid, securely supplied API key and a model available to that key.

## Run
From `Task4/`, create and activate a virtual environment, install dependencies using `python -m pip install -r requirements.txt`, then:
```bash
python agent.py --offline
streamlit run streamlit_app.py
python -m unittest discover -s tests -v
```
For the assessment's LLM requirement, configure a valid `GEMINI_API_KEY` through an environment variable or Streamlit secrets and test Gemini mode. Do not use the offline parser as evidence that LLM mode has been verified.

## Security issue requiring correction before submission
The reviewed ZIP includes a `Task4/.env` file and the source code in `agent.py` appears to contain a hard-coded API credential. Do not distribute either. Remove the real `.env` from the package, remove the hard-coded credential, load the key only from an environment variable or secrets store, and use `.env.example` containing a placeholder only. If the embedded or packaged credential is real, revoke/rotate it before further use. Never include the secret in screenshots, reports, or repository history.

## Limitations
This is an assessment prototype. It has no authentication, production deployment configuration, or database writes. Gemini mode depends on network access, API permissions, quota, and an available model name.

## Suggested demonstration
Run the offline tests, show one supported question, then show the live Gemini path separately. Demonstrate department count, average salary, highest-paid employee, a proposed raise, an unsupported request, and a missing/invalid-data case. Confirm that the source CSV remains unchanged after a proposed raise.
