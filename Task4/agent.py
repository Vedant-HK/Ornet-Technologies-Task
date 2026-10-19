"""Command-line AI Data Assistant: LLM intent parsing + deterministic Python tools."""
import json
import os
import re
from pathlib import Path
from dotenv import load_dotenv
from dataclasses import dataclass
from typing import Optional

PROJECT_DIR = Path(__file__).resolve().parent
load_dotenv(PROJECT_DIR / ".env")

from employee_tools import (
    average_salary,
    employee_count_by_department,
    highest_paid_employee,
    load_employees,
    proposed_salary_increase,
)


@dataclass
class Intent:
    tool: str
    department: Optional[str] = None
    percentage: Optional[float] = None
    error: Optional[str] = None


ALLOWED_TOOLS = {
    "employee_count",
    "average_salary",
    "highest_paid_employee",
    "proposed_salary_increase",
}


def _parse_json_object(text):
    """Parse JSON, tolerating a surrounding Markdown code fence."""
    cleaned = text.strip()
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", cleaned, flags=re.IGNORECASE)
    result = json.loads(cleaned)
    if not isinstance(result, dict):
        raise ValueError("LLM response must be a JSON object.")
    return result


class GeminiIntentParser:
    """Uses Gemini only to map natural language to a constrained tool request."""

    def __init__(self, api_key="GEMINI_API_KEY", model="gemini-3.8-flash"):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model = model
        if not self.api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is not set. Set it to enable LLM mode, or use --offline for local testing."
            )

    def parse(self, question):
        try:
            from google import genai
        except ImportError as exc:
            raise RuntimeError(
                "Gemini SDK is missing. Install dependencies with: python -m pip install -r requirements.txt"
            ) from exc

        prompt = f"""
You route employee-data questions to tools. Return ONLY one JSON object with keys:
tool, department, percentage.
Allowed tool values: employee_count, average_salary, highest_paid_employee,
proposed_salary_increase, unsupported.
department must be a department name or null. percentage must be a number or null.
Choose proposed_salary_increase only when the user explicitly asks to calculate/model a raise.
Do not answer the user's question and do not calculate any results.
If the request is outside the supported employee-data operations, choose unsupported.
Question: {question}
"""
        try:
            client = genai.Client(api_key=self.api_key)
            response = client.models.generate_content(
                model=self.model,
                contents=prompt,
                config={"response_mime_type": "application/json"},
            )
            data = _parse_json_object(response.text or "")
        except (json.JSONDecodeError, ValueError) as exc:
            raise RuntimeError("Gemini returned an invalid response. Please rephrase the question and try again.") from exc
        except Exception as exc:
            # Provide useful diagnostics without ever displaying the API key.
            message = str(exc).casefold()
            status = getattr(exc, "code", None) or getattr(exc, "status_code", None)

            if status in (400, 401, 403) or any(
                phrase in message for phrase in (
                    "api key not valid", "invalid api key", "unauthenticated",
                    "permission denied", "api_key_invalid", "unauthorized",
                )
            ):
                detail = (
                    "Gemini rejected the API key or its permissions. Create/check the key in "
                    "Google AI Studio, ensure it is copied completely, and confirm it is enabled "
                    "for the Gemini API."
                )
            elif status == 404 or "model not found" in message or "not supported for generatecontent" in message:
                detail = (
                    f"The Gemini model '{self.model}' was not found or is unavailable to this key. "
                    "Check the model name and use a model available to your API key."
                )
            elif any(phrase in message for phrase in (
                "quota", "resource_exhausted", "rate limit", "too many requests",
            )) or status == 429:
                detail = (
                    "Gemini rate limit or quota reached. Check the project's Gemini API quota/billing "
                    "and try again later."
                )
            elif any(phrase in message for phrase in (
                "connection", "timed out", "timeout", "network", "dns", "ssl",
            )):
                detail = (
                    "Could not connect to Gemini. Check internet access, VPN/firewall settings, "
                    "and retry."
                )
            else:
                # Include the exception class for troubleshooting but not request headers or secrets.
                detail = (
                    f"Gemini request failed ({type(exc).__name__}). Check the API key, model access, "
                    "quota, and internet connection. For more details, inspect the terminal output."
                )
            print(f"Gemini diagnostic: {type(exc).__name__}: {exc}")
            raise RuntimeError(detail) from exc
        tool = data.get("tool")
        if tool not in ALLOWED_TOOLS and tool != "unsupported":
            return Intent("unsupported", error="The request could not be mapped to a supported operation.")
        department = data.get("department")
        percentage = data.get("percentage")
        if department is not None and not isinstance(department, str):
            return Intent("unsupported", error="The department value returned by the LLM was invalid.")
        if percentage is not None:
            try:
                percentage = float(percentage)
            except (TypeError, ValueError):
                return Intent("unsupported", error="The percentage returned by the LLM was invalid.")
            if not 0 <= percentage <= 100:
                return Intent("unsupported", error="Please use a salary increase percentage between 0 and 100.")
        return Intent(tool, department, percentage)


def parse_intent_offline(question):
    """Small deterministic parser used for tests and runs without an API key."""
    q = question.casefold().strip()
    # Include the departments used in the bundled dataset, plus common HR alias.
    departments = [
        "customer support", "data science", "administration", "engineering",
        "operations", "product", "marketing", "finance", "human resources",
        "legal", "sales", "hr", "it",
    ]
    department = next((d for d in departments if re.search(rf"\b{re.escape(d)}\b", q)), None)
    if department == "human resources":
        department = "HR"
    elif department:
        department = department.upper() if department in {"hr", "it"} else department.title()

    if any(word in q for word in ("raise", "increase", "salary hike", "salary increment")):
        match = re.search(r"(\d+(?:\.\d+)?)\s*%", q)
        if not department or not match:
            return Intent("unsupported", error="Please specify a department and a percentage, e.g. '10% salary increase for HR'.")
        return Intent("proposed_salary_increase", department, float(match.group(1)))
    if "highest paid" in q or "highest-paid" in q or "highest salary" in q or "earns the most" in q:
        return Intent("highest_paid_employee")
    if "average salary" in q or "mean salary" in q or "average pay" in q:
        return Intent("average_salary")
    if "how many" in q or "count" in q or "number of employees" in q:
        if not department:
            return Intent("unsupported", error="Please specify a department for the employee count.")
        return Intent("employee_count", department)
    return Intent("unsupported", error="I can count employees by department, calculate average salary, find the highest-paid employee, or model a proposed department salary increase.")


def format_result(intent, result):
    """Convert tool results into concise, user-friendly messages."""
    if intent.tool == "employee_count":
        return f"There are {result['count']} employee records in {result['department']}."
    if intent.tool == "average_salary":
        if result["average_salary"] is None:
            return "I couldn't calculate the average salary because no valid salaries are available."
        return (
            f"The average salary is ₹{result['average_salary']:,.2f}, "
            f"based on {result['employees_with_salary']} employees with valid salary data."
        )
    if intent.tool == "highest_paid_employee":
        if result is None:
            return "I couldn't find an employee with a valid salary."
        return (
            f"The highest-paid employee is {result['name']} "
            f"({result['department']}), with a salary of ₹{result['salary']:,.2f}."
        )
    if intent.tool == "proposed_salary_increase":
        lines = [f"Proposed {result['percentage']:g}% salary increase for {result['department']}:"]
        for employee in result["employees"]:
            if employee["proposed_salary"] is None:
                reason = employee.get("message", "salary is unavailable")
                lines.append(f"- {employee['name']}: skipped ({reason.rstrip('.').lower()}).")
            else:
                lines.append(
                    f"- {employee['name']}: ₹{employee['current_salary']:,.2f} → "
                    f"₹{employee['proposed_salary']:,.2f} "
                    f"(increase: ₹{employee['increase_amount']:,.2f})"
                )
        lines.append(result["note"])
        return "\n".join(lines)
    return intent.error or "Sorry, I can't handle that request. Please try a supported employee-data question."


class EmployeeDataAssistant:
    def __init__(self, df, intent_parser):
        self.df = df
        self.intent_parser = intent_parser

    def answer(self, question):
        if not isinstance(question, str) or not question.strip():
            return "Please enter a question."
        try:
            intent = self.intent_parser.parse(question)
            if intent.error:
                return intent.error
            if intent.tool == "employee_count":
                if not intent.department:
                    return "Please specify a department."
                result = employee_count_by_department(self.df, intent.department)
            elif intent.tool == "average_salary":
                result = average_salary(self.df)
            elif intent.tool == "highest_paid_employee":
                result = highest_paid_employee(self.df)
            elif intent.tool == "proposed_salary_increase":
                if not intent.department or intent.percentage is None:
                    return "Please specify a department and a percentage."
                result = proposed_salary_increase(self.df, intent.department, intent.percentage)
            else:
                return "Sorry, I can't handle that request. Please try a supported employee-data question."
            return format_result(intent, result)
        except (ValueError, TypeError, json.JSONDecodeError) as exc:
            return f"Could not process the request: {exc}"
        except RuntimeError as exc:
            return str(exc)


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Ask questions about the sample employee dataset.")
    parser.add_argument("--offline", action="store_true", help="Use a small local parser; no LLM/API key required.")
    args = parser.parse_args()

    df = load_employees()
    if args.offline:
        intent_parser = type("OfflineParser", (), {"parse": staticmethod(parse_intent_offline)})()
        mode = "offline"
    else:
        intent_parser = GeminiIntentParser()
        mode = "Gemini LLM"
    assistant = EmployeeDataAssistant(df, intent_parser)
    print(f"Employee Data Assistant ({mode}). Type 'exit' to quit.")
    print("Try: How many employees are in IT? | What is the average salary? | Who is highest-paid?")
    while True:
        try:
            question = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            break
        if question.casefold() in {"exit", "quit"}:
            print("Goodbye.")
            break
        print("Assistant:", assistant.answer(question))


if __name__ == "__main__":
    main()
