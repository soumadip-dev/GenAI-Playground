import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from rich import print

# REACT agent:  
# Think => Act => Observe => repeat

# Load environment variables from the .env file.
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is not configured.")

# Initialize the Gemini client.
gemini_client = genai.Client(api_key=API_KEY)

print("[bold cyan]=" * 60 + "[/bold cyan]")
print("[bold magenta]  Career Agent - Skills, Certifications, Projects & Salary[/bold magenta]")
print("[bold cyan]=" * 60 + "[/bold cyan]")


# Return the required skills for a career goal.
def get_skills(goal: str) -> str:
    """Retrieve the core skills required for a career goal.

    Args:
        goal: The user's target career goal.

    Returns:
        A formatted list of required skills.
    """
    return """
Required Skills:
- Python
- Machine Learning
- Statistics
- Generative AI
- Prompt Engineering
- Retrieval-Augmented Generation (RAG)
"""


# Return recommended certifications for a career goal.
def get_certificate(goal: str) -> str:
    """Retrieve recommended certifications for a career goal.

    Args:
        goal: The user's target career goal.

    Returns:
        A formatted list of recommended certifications.
    """
    return """
Recommended Certifications:
- AI-102
- AZ-204
- AWS AI Practitioner
- Google Gen AI
"""


# Return the estimated salary range for a career goal.
def get_salary(goal: str) -> str:
    """Retrieve the estimated salary range for a career goal.

    Args:
        goal: The user's target career goal.

    Returns:
        A formatted salary range.
    """
    return """
Salary Expectations:
- Entry Level: 8–12 LPA
- Mid Level: 15–25 LPA
- Senior Level: 30+ LPA
"""


# Return recommended projects for a career goal.
def get_project_recommendations(goal: str) -> str:
    """Retrieve project recommendations for a career goal.

    Args:
        goal: The user's target career goal.

    Returns:
        A formatted list of recommended projects.
    """
    return """
Recommended Projects:
- AI Chatbot
- PDF RAG Assistant
- Research Agent
- Career Coach Agent
"""


# Register all available tools.
TOOL_REGISTRY = {
    "SKILL_TOOL": get_skills,
    "CERTIFICATION_TOOL": get_certificate,
    "PROJECT_TOOL": get_project_recommendations,
    "SALARY_TOOL": get_salary,
}


# AI agent responsible for providing career guidance.
class CareerCoachAgent:
    def __init__(self, goal: str):
        # Store the user's career goal.
        self.goal = goal
        self.observation = []

    # Think
    def think(self):
        prompt = f"""
You are a career coach agent helping a user to achieve their goal.
User Goal: {self.goal}

Available Tools:
SKILL_TOOL: Returns the required skills for a career goal.
CERTIFICATION_TOOL: Returns recommended certifications for a career goal.
PROJECT_TOOL: Returns recommended projects for a career goal.
SALARY_TOOL: Returns the estimated salary range for a career goal.

Previous Observations:
{self.observation}

Think Carefully and decide what information you still need to gather.

Return Only one word from this list: 
SKILL_TOOL
CERTIFICATION_TOOL
PROJECT_TOOL
SALARY_TOOL
FINISH
"""
        response = gemini_client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt,
        )

        return response.text

    # Action
    def execute_action(self, action):
        tool = TOOL_REGISTRY.get(action)

        if tool:
            return tool(self.goal)
        else:
            return None

    # Final response 
    def generate_final_plan(self):
        prompt = f"""
            User Goal: {self.goal}
            Collected Information: {self.observation}

            Generate:
            1. Career Summary
            2. Skills Required
            3. Certifications Recommended
            4. Projects Recommended
            5. Salary Expectations
            6. 90-Day Learning Roadmap

            Formatting constraints:
            - Return plain text only.
            - Do not use any Markdown formatting (no asterisks, hash tags, or bolding).
            - Keep responses concise and brief.( as short as possible)
"""

        response = gemini_client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt,
        )

        print("\n[bold green]" + "=" * 60 + "[/bold green]")
        print("[bold white on green]                 FINAL CAREER PLAN                  [/bold white on green]")
        print("[bold green]" + "=" * 60 + "[/bold green]")

        return response.text

    # react pattern
    def run(self):
        step = 1
        while True:
            print("\n[dim]" + "-" * 60 + "[/dim]")
            print(f"[bold yellow]STEP {step}[/bold yellow]")
            print("[dim]" + "-" * 60 + "[/dim]")

            # Think
            action = self.think()
            print(f"[bold blue][THOUGHT RESULT]:[/bold blue] [cyan]{action}[/cyan]")

            # Finish
            if action == "FINISH":
                print("\n[bold green][STATUS]:[/bold green] [italic]Enough information collected. Exiting loop...[/italic]")
                break

            # Action
            print(f"[bold magenta][ACTION]:[/bold magenta] Executing [bold cyan]{action}[/bold cyan]")
            result = self.execute_action(action)

            # Observation
            print(f"[bold white on blue][OBSERVATION]:[/bold white on blue]")
            if result:
                print(f"[green]{result.strip()}[/green]")
                self.observation.append(result.strip())
            else:
                print(f"[bold red]Unknown action or tool output failed for: {action}[/bold red]")
                self.observation.append(f"Attempted {action}, but no valid data returned.")
            
            step += 1

        final_plan = self.generate_final_plan()
        print(f"[bold bright_white]{final_plan}[/bold bright_white]")


goal = input("Enter your career goal: ")
career_coach = CareerCoachAgent(goal)
career_coach.run()