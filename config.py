import os

def setup_environment(gemini_api_key: str):
    """Sets environment variables for CrewAI to use Gemini v1beta OpenAI-compatible endpoints."""
    os.environ["GEMINI_API_KEY"] = gemini_api_key
    os.environ["OPENAI_API_BASE"] = "https://generativelanguage.googleapis.com/v1beta/openai/"
    os.environ["OPENAI_API_KEY"] = gemini_api_key
    os.environ["OPENAI_MODEL_NAME"] = "gemini-2.5-flash"
