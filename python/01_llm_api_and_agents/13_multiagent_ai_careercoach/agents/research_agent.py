"""
Research Agent

Responsibility:
Perform detailed research based on the planner's execution plan.
"""

from agents.base_agent import BaseAgent
from prompts.research_prompt import RESEARCH_PROMPT


class ResearchAgent(BaseAgent):

    def get_agent_name(self) -> str:
        return "Researcher"

    def get_memory_key(self) -> str:
        return "researcher"

    def build_prompt(self) -> str:
        planner_response = self.memory.get("planner")
        return RESEARCH_PROMPT.format(planner_output=planner_response)
