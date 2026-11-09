import os
from time import sleep

from dotenv import load_dotenv
from google import genai
from rich import print

# Load environment variables from the .env file
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is not configured.")

# Initialize the Gemini client
gemini_client = genai.Client(api_key=API_KEY)


# AI agent that generates a learning roadmap based on a user's goal.
class RoadmapAgent:
    def __init__(self, goal: str):
        # Store the user's learning goal.
        self.goal = goal

    # Analyze the goal and identify the required skills. [Reasoning Phase]
    def reason(self):
        print(
            "[bold yellow]Agent:[/bold yellow] Analyzing your goal and identifying the required skills..."
        )

        prompt = f"""
        User Goal: {self.goal}

        Identify all the skills required to achieve this goal.

        Return only the list of skills.
        """

        response = gemini_client.interactions.create(
            model="gemini-3.5-flash-lite",
            input=prompt,
        )

        return response.output_text  # type: ignore

    # Organize the identified skills into an effective learning sequence.[Planing Phase]
    def plan(self, skills):
        print("[bold cyan]Agent:[/bold cyan] Creating the optimal learning sequence...")

        prompt = f"""
        Goal: {self.goal}

        Skills:
        {skills}

        Arrange the skills in the best learning order.
        """

        response = gemini_client.interactions.create(
            model="gemini-3.5-flash-lite",
            input=prompt,
        )

        return response.output_text  # type: ignore

    # Generate the final 90-day learning roadmap. [Execution Phase]
    def execute(self, learning_plan):
        print(
            "[bold magenta]Agent:[/bold magenta] Generating your 90-day learning roadmap..."
        )

        prompt = f"""
        Goal: {self.goal}

        Learning Plan:
        {learning_plan}

        Create a detailed 90-day learning roadmap.

        Return the roadmap in simple and short sentences.
        Do not use Markdown formatting.
        """

        response = gemini_client.interactions.create(
            model="gemini-3.5-flash-lite",
            input=prompt,
        )

        return response.output_text  # type: ignore

    # Execute the complete roadmap generation workflow.
    def run(self):
        skills = self.reason()
        sleep(1)

        learning_plan = self.plan(skills)
        sleep(1)

        roadmap = self.execute(learning_plan)
        sleep(1)

        print()
        print("[bold green]" + "=" * 60 + "[/bold green]")
        print("[bold green]Final 90-Day Learning Roadmap[/bold green]")
        print("[bold green]" + "=" * 60 + "[/bold green]")
        print(roadmap)


print("[bold blue]Welcome to the AI Roadmap Generator![/bold blue]")

goal = input("Enter your learning goal: ")

agent = RoadmapAgent(goal)
agent.run()
