"""
Gemini Service
Responsible for interacting with Gemini API
"""

from google import genai
from google.genai import types
from config import Config


class GeminiService:
    """Wrapper around Gemini API"""

    def __init__(self):
        Config.validate()
        self.gemini_client = genai.Client(api_key=Config.GEMINI_API_KEY)

    def generate_response(self, prompt: str) -> str | None:
        """Send prompt to Gemini API and get response

        Args:
            prompt (str): Prompt to send to Gemini API

        Returns:
            str: AI generated response from Gemini API
        """
        try:
            response = self.gemini_client.models.generate_content(
                model=Config.MODEL_NAME,
                contents=prompt,
            )
            return response.text
        except Exception as ex:
            raise RuntimeError(f"Gemini API Error: {ex}")
