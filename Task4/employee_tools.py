"""Deterministic employee-data tools. Calculations are performed in Python, not by the LLM."""
from pathlib import Path
import pandas as pd

REQUIRED_COLUMNS = {"employee_id", "name", "department", "salary", "age"}
DEFAULT_DATA_PATH = Path(__file__).parent / "data" / "employees.csv"


class DataValidationError(ValueError):
    """Raised when the employee dataset is missing required structure."""


def load_employees(path=DEFAULT_DATA_PATH):
    """Load and validate employee data, treating invalid numeric values as missing."""
    try:
        df = pd.read_csv(path)
    except FileNotFoundError as exc:
        raise DataValidationError(f"Employee data file not found: {path}") from exc
    except (pd.errors.ParserError, UnicodeDecodeError) as exc:
        raise DataValidationError(f"Could not read employee data: {exc}") from exc

    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise DataValidationError(
            "Employee data is missing required columns: " + ", ".join(sorted(missing))
        )

    df = df.copy()
    df["department"] = df["department"].astype("string").str.strip()
    df["name"] = df["name"].astype("string").str.strip()
    df["salary"] = pd.to_numeric(df["salary"], errors="coerce")
    df["employee_id"] = pd.to_numeric(df["employee_id"], errors="coerce")
    return df


def employee_count_by_department(df, department):
    """Return the number of employee records for a department, case-insensitively."""
    department = _validate_department(department)
    matches = df[df["department"].str.casefold() == department.casefold()]
    if matches.empty:
        return {"department": department, "count": 0}
    return {"department": department, "count": int(len(matches))}


def average_salary(df):
    """Return the mean of non-missing, non-negative salaries."""
    salaries = df.loc[df["salary"].notna() & (df["salary"] >= 0), "salary"]
    if salaries.empty:
        return {"average_salary": None, "employees_with_salary": 0}
    return {
        "average_salary": float(salaries.mean()),
        "employees_with_salary": int(salaries.count()),
    }


def highest_paid_employee(df):
    """Return the highest-paid employee among records with valid salaries."""
    eligible = df.dropna(subset=["salary", "name"])
    eligible = eligible[eligible["salary"] >= 0]
    if eligible.empty:
        return None
    row = eligible.loc[eligible["salary"].idxmax()]
    return {
        "employee_id": int(row["employee_id"]) if pd.notna(row["employee_id"]) else None,
        "name": str(row["name"]),
        "department": str(row["department"]),
        "salary": float(row["salary"]),
    }


def proposed_salary_increase(df, department, percentage):
    """Calculate a proposal only; never writes back to the dataset or a database."""
    department = _validate_department(department)
    try:
        percentage = float(percentage)
    except (TypeError, ValueError) as exc:
        raise ValueError("Percentage must be a number.") from exc
    if not 0 <= percentage <= 100:
        raise ValueError("Percentage must be between 0 and 100.")

    matches = df[df["department"].str.casefold() == department.casefold()].copy()
    if matches.empty:
        return {"department": department, "employees": [], "message": "No matching employees."}

    employees = []
    for _, row in matches.iterrows():
        if pd.isna(row["salary"]) or float(row["salary"]) < 0:
            reason = "salary is missing" if pd.isna(row["salary"]) else "salary is invalid"
            employees.append({
                "name": str(row["name"]),
                "current_salary": None,
                "proposed_salary": None,
                "message": f"Skipped because {reason}.",
            })
            continue
        current = float(row["salary"])
        employees.append({
            "name": str(row["name"]),
            "current_salary": current,
            "proposed_salary": round(current * (1 + percentage / 100), 2),
            "increase_amount": round(current * percentage / 100, 2),
        })
    return {
        "department": department,
        "percentage": percentage,
        "employees": employees,
        "note": "Proposal only. No employee records were modified.",
    }


def _validate_department(department):
    if not isinstance(department, str) or not department.strip():
        raise ValueError("Please specify a department.")
    return department.strip()
