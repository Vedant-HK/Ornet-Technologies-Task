# Task 4: Mini AI Data Assistant

A small employee-data assistant with a Streamlit chat interface and a command-line option. In Gemini mode, an LLM maps natural-language questions to a limited set of tools. Python performs all calculations; the LLM does not invent employee counts or salary values.

## Features

- Count employees by department.
- Calculate average salary using available salary values.
- Find the highest-paid employee among records with valid salaries.
- Calculate proposed department salary increases without changing source data.
- Handle unsupported questions, missing or negative salaries, invalid percentages, Gemini/API failures, and missing files/columns.
- Unit tests cover tools and at least five example questions.

## Project structure

```text
Task4_AI_Data_Assistant/
├── data/employees.csv
├── employee_tools.py
├── agent.py
├── streamlit_app.py
├── tests/test_agent.py
├── requirements.txt
├── .env.example
└── README.md
```

## Setup

Use Python 3.10 or newer.

```bash
python -m venv .venv
```

Activate the environment, then install dependencies:

```bash
# Windows PowerShell
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt

# macOS/Linux
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Run with Gemini (LLM mode)

Set an API key in the environment. Obtain the key from Google AI Studio; never hard-code or commit it.

```powershell
# Windows PowerShell — current terminal session only
$env:GEMINI_API_KEY="your_api_key"
python agent.py
```

```bash
# macOS/Linux — current terminal session only
export GEMINI_API_KEY="your_api_key"
python agent.py
```

The app defaults to `gemini-3.8-flash`, based on the model availability error returned by the configured Gemini API. If that model is not enabled for your account, change the default in `GeminiIntentParser` in `agent.py` to a model listed as available to your API key. The LLM returns a constrained JSON intent (`tool`, `department`, `percentage`). The application validates the intent and dispatches to a Python tool. Only the tool output is used to report calculated results.

## Run the Streamlit interface

From the project root, run:

```bash
streamlit run streamlit_app.py
```

The app opens in your browser. Use **Gemini LLM** mode for natural-language intent routing, or choose **Offline demo** to try supported example questions without an API key. To use a local key, create a `.env` file in the project root based on `.env.example`; do not commit the real key. The app also supports `GEMINI_API_KEY` through Streamlit secrets.

## Run offline (no API key)

The offline parser exists for local demonstrations and tests. It is a lightweight intent parser, not a substitute for the LLM requirement in the assessment.

```bash
python agent.py --offline
```

## Run tests

From the project root:

```bash
python -m unittest discover -s tests -v
```

Tests use the offline parser and do not call an external API.

## Example questions

1. `How many employees are in the IT department?` (18 employee records in the supplied dataset)
2. `What is the average salary?` (₹101,349.21, excluding missing and negative salaries)
3. `Who is the highest-paid employee?` (Rahul Ansari, ₹221,000.00)
4. `Calculate a 10% salary increase for the HR department.`
5. `What is the weather today?` (unsupported request)
6. `Calculate a 10% salary increase for IT.` (demonstrates missing salary handling)

## Data handling and assumptions

- The bundled `data/employees.csv` is the supplied 200-row employee dataset. It contains 12 departments and includes 8 missing salaries, 3 negative salary values, and 6 missing ages. Salary calculations exclude missing and negative salaries.
- Average salary excludes missing, non-numeric, and negative salaries.
- Highest-paid lookup excludes records with missing or negative salaries.
- Proposed raises skip employees whose salary is missing or negative.
- Department matching is case-insensitive.
- Employee count counts rows/records for the department; duplicates are not silently removed.
- Proposed raises are calculations only. The app never writes changes to the CSV or a database.
- Salary increase percentages must be between 0 and 100.
- The LLM API is used for intent/tool selection only. Python executes the calculation and formats the answer.

## Limitations

- Gemini LLM mode requires network access, an API key, and the `google-genai` SDK.
- The offline parser supports common example phrasings only and is intended for demonstrations/tests.
- The prototype has no database writes, authentication, or production deployment configuration.

## AI assistance disclosure

An AI coding assistant was used to help draft and review the implementation and documentation.

### Troubleshooting Gemini API errors

- Keep `.env` in the same folder as `streamlit_app.py` and `agent.py`.
- The filename must be exactly `.env`, not `.env.txt`. In Windows File Explorer, enable **View → Show → File name extensions** to check.
- Use this exact format with no quotes or extra spaces around the variable name: `GEMINI_API_KEY=your_actual_key`.
- Do not paste the key into chat, screenshots, source code, or Git.
- Stop Streamlit with `Ctrl+C` and restart it after changing `.env`.
- The sidebar should say **Gemini API key detected**. This only confirms a value was loaded; it does not prove the key is valid.
- The updated app shows a more specific error category for invalid keys/permissions, unavailable models, quota limits, or connection failures. The terminal also prints the provider exception for local debugging; check it privately and never share your API key.
