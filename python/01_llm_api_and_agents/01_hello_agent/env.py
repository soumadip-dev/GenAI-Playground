import os
from typing import Literal, TypedDict
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

Provider = Literal["openai", "gemini", "groq"]


class Env(TypedDict):
    OPENAI_API_KEY: str
    GEMINI_API_KEY: str
    GROQ_API_KEY: str
    PROVIDER: Provider


provider = os.getenv("PROVIDER", "openai").lower()

env: Env = {
    "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY", ""),
    "GEMINI_API_KEY": os.getenv("GEMINI_API_KEY", ""),
    "GROQ_API_KEY": os.getenv("GROQ_API_KEY", ""),
    "PROVIDER": provider if provider in ["openai", "gemini", "groq"] else "openai",
}
