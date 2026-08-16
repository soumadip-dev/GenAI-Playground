# Receive input -> Create prompt -> Call Gemini -> Return response

"""
Base Agent

All AI agents should inherit from this class and implement
the execute() method.
"""

from abc import ABC, abstractmethod

from memory.shared_memory import SharedMemory
from services.gemini_service import GeminiService


class BaseAgent(ABC):
    """
    Abstract base class for all AI agents.
    """

    def __init__(self, memory: SharedMemory):
        super().__init__()
        self.memory = memory
        self.gemini = GeminiService()

    @abstractmethod
    def execute(self) -> str:
        """
        Execute the agent's logic and return the final response.
        """
        pass

    def ask_gemini(self, prompt: str) -> str:
        """
        Send a prompt to Gemini and return its response.

        Returns an empty string if Gemini does not return a response.
        """
        return self.gemini.generate_response(prompt) or ""
