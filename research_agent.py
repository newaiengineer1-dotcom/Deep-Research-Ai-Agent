import os
import re

import streamlit as st
from crewai import Agent, Crew, LLM, Process, Task

from search_tool import DuckDuckGoResearchTool


MODEL_NAME = "groq/openai/gpt-oss-120b"


def get_groq_api_key():
    key = os.getenv("GROQ_API_KEY")

    if key:
        return key

    try:
        return st.secrets["GROQ_API_KEY"]
    except Exception:
        return None


def build_llm():
    api_key = get_groq_api_key()

    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is missing. Add GROQ_API_KEY to Streamlit Secrets."
        )

    return LLM(
        model=MODEL_NAME,
        api_key=api_key,
        temperature=0.2,
        max_tokens=12000,
    )
