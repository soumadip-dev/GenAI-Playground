"""
Agent Orchestrator

Responsible for managing and executing AI agents in sequence.
"""

from typing import List

from rich import print

from agents.base_agent import BaseAgent
from memory.shared_memory import SharedMemory


class AgentOrchestrator:
    """
    Manage and execute AI agents in sequence.
    """

    def __init__(self, memory: SharedMemory) -> None:
        """
        Initialize the agent orchestrator.

        Args:
            memory: Shared memory accessible by all agents.
        """
        self.memory = memory
        self.agents: List[BaseAgent] = []

    def register(self, agent: BaseAgent) -> None:
        """
        Register an AI agent with the orchestrator.

        Args:
            agent: Agent to register.
        """
        self.agents.append(agent)

    def execute(self):
        """
        Execute all registered agents in sequence.

        Returns:
            The final response stored in shared memory.
        """
        print("[bold cyan]Starting Multi-Agent Workflow[/bold cyan]")

        for agent in self.agents:
            print(f"[blue]Executing {agent.get_agent_name()} Agent...[/blue]")

            response = agent.execute()

        print("[bold green]Multi-Agent Workflow Completed[/bold green]")

        return self.memory.get("reviewer")
