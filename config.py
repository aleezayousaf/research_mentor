import os
import streamlit as st

def setup_environment(gemini_api_key: str = None, model_name: str = "gemini-3.8-flash"):
    """
    Sets environment variables for CrewAI to use Gemini endpoints.
    
    Supported models:
      - 'gemini-3.8-flash' (High reasoning & agentic tasks)
      - 'gemini-3.5-flash-lite' (Ultra-fast, lower latency)
    """
    # 1. Fetch Key from argument, Streamlit Secrets, or System Env
    api_key = gemini_api_key
    if not api_key and "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
    if not api_key:
        api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return False

    # 2. Configure LiteLLM / CrewAI OpenAI-compatible bridge
    os.environ["GEMINI_API_KEY"] = api_key
    os.environ["OPENAI_API_BASE"] = "https://generativelanguage.googleapis.com/v1beta/openai/"
    os.environ["OPENAI_API_KEY"] = api_key
    
    # Provider prefix format required by LiteLLM in CrewAI
    os.environ["OPENAI_MODEL_NAME"] = f"gemini/{model_name}"

    return True
