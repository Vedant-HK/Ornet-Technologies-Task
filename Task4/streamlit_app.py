"""Streamlit interface for the employee-data assistant."""
import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from agent import EmployeeDataAssistant, GeminiIntentParser, parse_intent_offline
from employee_tools import load_employees

PROJECT_DIR = Path(__file__).resolve().parent
load_dotenv(dotenv_path=PROJECT_DIR / ".env", override=False)

st.set_page_config(
    page_title="Employee Data Assistant",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
      .block-container {max-width: 1120px; padding-top: 2rem; padding-bottom: 2rem;}
      .hero {padding: 1.5rem 1.7rem; border: 1px solid rgba(128,128,128,.22);
             border-radius: 18px; margin-bottom: 1.2rem;
             background: linear-gradient(120deg, rgba(80,120,220,.12), rgba(50,180,160,.07));}
      .hero h1 {margin: 0 0 .4rem 0; letter-spacing: -.03em;}
      .hero p {margin: 0; opacity: .8; font-size: 1.02rem;}
      [data-testid="stChatMessage"] {border-radius: 14px;}
      .metric-note {font-size: .82rem; opacity: .72;}
      div[data-testid="stMetric"] {border: 1px solid rgba(128,128,128,.2); padding: 14px 16px; border-radius: 14px;}
    </style>
    """,
    unsafe_allow_html=True,
)


def get_api_key():
    """Read the key from environment or Streamlit secrets without displaying it."""
    key = os.getenv("GEMINI_API_KEY", "").strip()
    if key:
        return key
    try:
        return str(st.secrets.get("GEMINI_API_KEY", "")).strip()
    except (FileNotFoundError, AttributeError):
        return ""


@st.cache_data(show_spinner=False)
def get_employee_data():
    return load_employees(PROJECT_DIR / "data" / "employees.csv")


def build_assistant(mode, api_key, df):
    if mode == "Gemini LLM":
        parser = GeminiIntentParser(api_key=api_key)
    else:
        parser = type("OfflineParser", (), {"parse": staticmethod(parse_intent_offline)})()
    return EmployeeDataAssistant(df, parser)


def queue_question(question):
    st.session_state.pending_question = question


try:
    employees = get_employee_data()
except (OSError, ValueError) as exc:
    st.error(f"The employee dataset could not be loaded: {exc}")
    st.stop()

api_key = get_api_key()
default_mode = "Gemini LLM" if api_key else "Offline demo"

with st.sidebar:
    st.markdown("### ⚙️ Assistant settings")
    mode = st.radio(
        "Processing mode",
        ["Gemini LLM", "Offline demo"],
        index=0 if default_mode == "Gemini LLM" else 1,
        help="Gemini maps natural-language questions to tools. Offline demo uses a small rule-based parser.",
    )
    if mode == "Gemini LLM":
        if api_key:
            st.success("Gemini API key detected")
        else:
            st.warning("Gemini API key not found")
            st.caption("Create a file named exactly .env (not .env.txt) beside streamlit_app.py, add GEMINI_API_KEY=your_real_key, save it, then stop and restart Streamlit.")
    else:
        st.info("Offline demo mode · no API call")

    st.divider()
    st.markdown("### 📁 Dataset overview")
    st.metric("Employee records", len(employees))
    st.metric("Departments", employees["department"].nunique())
    st.caption("The bundled employee CSV is used for all tool calculations. Missing and negative salaries are excluded from salary calculations.")
    st.divider()
    st.markdown("### 🛡️ Data safety")
    st.caption("All counts and salary calculations are performed by Python. Proposed raises never modify the CSV.")
    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pending_question = None
        st.rerun()

st.markdown(
    """
    <div class="hero">
      <h1>📊 Employee Data Assistant</h1>
      <p>Ask questions about your employee dataset in plain English. Answers are grounded in Python tool results.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

metric_cols = st.columns(3)
with metric_cols[0]:
    st.metric("Employee records", len(employees))
with metric_cols[1]:
    st.metric("Departments", employees["department"].nunique())
with metric_cols[2]:
    st.metric("Processing mode", "Gemini LLM" if mode == "Gemini LLM" else "Offline demo")

st.markdown("#### Try a question")
quick_questions = [
    "How many employees are in the IT department?",
    "What is the average salary?",
    "Who is the highest-paid employee?",
    "Calculate a 10% salary increase for HR.",
    "How many employees are in Finance?",
    "How many employees are in Sales?",
    "What is the mean salary?",
    "Find the highest salary in the company.",
    "Calculate a 5% salary increase for Engineering.",
]
quick_cols = st.columns(2)
for index, question in enumerate(quick_questions):
    with quick_cols[index % 2]:
        st.button(question, key=f"quick_{index}", use_container_width=True, on_click=queue_question, args=(question,))

st.markdown("#### Conversation")
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pending_question" not in st.session_state:
    st.session_state.pending_question = None

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

submitted_question = st.chat_input("Ask about employee counts, salaries, or a proposed raise…")
question = submitted_question or st.session_state.pending_question
if question:
    st.session_state.pending_question = None
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        if mode == "Gemini LLM" and not api_key:
            answer = (
                "Gemini mode needs a `GEMINI_API_KEY`. Add it to a `.env` file in the project folder "
                "or choose **Offline demo** in the sidebar to try the supported examples without an API call."
            )
            st.warning(answer)
        else:
            try:
                assistant = build_assistant(mode, api_key, employees)
                with st.spinner("Checking the request and running the relevant tool…"):
                    answer = assistant.answer(question)
                st.markdown(answer)
            except (RuntimeError, ValueError) as exc:
                answer = f"I couldn't process that request: {exc}"
                st.error(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})

st.caption("Assessment prototype · Synthetic employee data · No employee records are changed by this assistant.")
