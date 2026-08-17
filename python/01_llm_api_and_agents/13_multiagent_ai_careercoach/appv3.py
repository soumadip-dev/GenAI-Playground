"""
AI Career Coach

Entry point for the AI Career Coach application.

This module initializes the required services and agents,
accepts career-related queries from the user, executes the
multi-agent career planning workflow, and displays the
final career roadmap.
"""

from rich import print

from agents.planner_agent import PlannerAgent
from agents.research_agent import ResearchAgent
from agents.reviewer_agent import ReviewerAgent
from agents.writer_agent import WriterAgent
from memory.conversation_memory import ConversationMemory
from memory.shared_memory import SharedMemory
from orchestrator.agent_orchestrator import AgentOrchestrator
from services.gemini_service import GeminiService


def main() -> None:
    """
    Run the AI Career Coach application.

    The application continuously accepts career-related queries
    until the user enters "exit" or "bye".

    Workflow:
        1. Initialize conversation memory and the Gemini service.
        2. Display the application header.
        3. Get the user's career goal.
        4. Check whether the user wants to exit.
        5. Initialize shared memory.
        6. Store the user's query in conversation and shared memory.
        7. Create the career planning agents.
        8. Register the agents with the orchestrator.
        9. Execute the multi-agent workflow.
        10. Display the final career roadmap.
        11. Store the final response in conversation memory.
    """

    # Initialize shared conversation memory and the Gemini service.
    conversation_memory = ConversationMemory()
    gemini_service = GeminiService()

    while True:
        # Display the application header.
        separator = "=" * 70
        print(f"\n[dim]{separator}[/dim]")
        print("[bold cyan]AI Career Coach[/bold cyan]")
        print(f"[dim]{separator}[/dim]")

        # Get the user's career goal or query.
        user_query = input("Enter your career goal: ").strip()

        # Exit the application when the user enters an exit command.
        if user_query.lower() in {"exit", "bye", "quit"}:
            print("[bold yellow]Exiting AI Career Coach...[/bold yellow]")
            break

        # Ignore empty user input and prompt the user again.
        if not user_query:
            print("[italic yellow]Please enter a career goal.[/italic yellow]")
            continue

        # Initialize shared memory for the current workflow.
        memory = SharedMemory()

        # Store the user's query in conversation memory so that
        # agents can access the conversation history.
        conversation_memory.add_user_message(user_query)

        # Store the user's query in shared memory so that agents
        # can access it while building their prompts.
        memory.add("user_query", user_query)

        # Create all agents using the shared memory,
        # conversation memory, and Gemini service.
        planner = PlannerAgent(
            memory,
            conversation_memory,
            gemini_service,
        )

        researcher = ResearchAgent(
            memory,
            conversation_memory,
            gemini_service,
        )

        writer = WriterAgent(
            memory,
            conversation_memory,
            gemini_service,
        )

        reviewer = ReviewerAgent(
            memory,
            conversation_memory,
            gemini_service,
        )

        # Create the orchestrator and initialize it with
        # the shared memory and conversation memory.
        orchestrator = AgentOrchestrator(
            memory,
            conversation_memory,
        )

        # Register the agents in the order in which
        # they should be executed.
        orchestrator.register(planner)
        orchestrator.register(researcher)
        orchestrator.register(writer)
        orchestrator.register(reviewer)

        # Execute the complete multi-agent workflow.
        final_response = orchestrator.execute()

        # Store the final AI response in conversation memory
        # so that it is available in subsequent conversations.
        conversation_memory.add_ai_message(final_response.output)

        # Display the final reviewed career roadmap.
        print(f"\n[dim]{separator}[/dim]")
        print("[bold green]FINAL CAREER ROADMAP[/bold green]")
        print(f"[dim]{separator}[/dim]")
        print(final_response.output)


if __name__ == "__main__":
    main()
