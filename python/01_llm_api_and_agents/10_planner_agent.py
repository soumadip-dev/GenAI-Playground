# Planner Agent: Here the agent will first plan which tools to use and which don't need according to the goal and then execute those tools.
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from rich import print

# Load environment variables from the .env file.
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is not configured.")

# Initialize the Gemini client.
gemini_client = genai.Client(api_key=API_KEY)

# Multiplies ONLY the '=' sign
print(f"[bold cyan]{'=' * 60}[/bold cyan]")
print("[bold magenta]   Career Agent - Skills, Certifications, Projects & Salary   [/bold magenta]")
print("[bold cyan]=" * 60 + "[/bold cyan]\n")


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
        self.plan = []

    def create_plan(self):
        print("[bold blue]" + "=" * 60 + "[/bold blue]")
        print("[bold blue]                   CREATING EXECUTION PLAN                    [/bold  blue]")
        print("[bold blue]" + "=" * 60 + "[/bold blue]\n")

        prompt = f"""
You are an expert AI Planner Agent responsible for breaking down a user's goal into an optimal, minimal execution plan.

### USER GOAL
{self.goal}

### AVAILABLE TOOLS
- SKILL_TOOL: Retrieves required technical and soft skills for a career goal.
- CERTIFICATION_TOOL: Retrieves industry-recognized certifications for a career goal.
- PROJECT_TOOL: Retrieves practical portfolio project ideas for a career goal.
- SALARY_TOOL: Retrieves estimated compensation ranges for a career goal.

### TASK
Analyze the user's goal. Decide which tools are necessary to gather all required information. Construct an execution sequence that uses ONLY essential tools.

### RULES
1. Select ONLY tools that directly address the specific intent of the user's goal.
2. DO NOT invoke unnecessary or redundant tools.
3. Output exactly ONE tool name per line in execution order.
4. Conclude the sequence with "FINISH" on a new line.
5. Strict Output Constraint: Do NOT include explanations, introduction, markdown blocks, thought process, or reasoning in your final output. Return ONLY the tool names followed by FINISH.

### EXAMPLES

Example 1:
User Goal: "What skills and certifications do I need to become a DevOps Engineer?"
Output:
SKILL_TOOL
CERTIFICATION_TOOL


Example 2:
User Goal: "How much can I earn as a Data Scientist and what projects should I build?"
Output:
SALARY_TOOL
PROJECT_TOOL
"""
        response = gemini_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        plan = []

        # AFTER
        text_content = response.text or ""
        for line in text_content.split("\n"):
            tool = line.strip()
            if tool in TOOL_REGISTRY:
                plan.append(tool)

        return plan

    # Execute plan
    def execute_plan(self):
        print("\n[bold magenta]" + "=" * 60 + "[/bold magenta]")
        print("[bold magenta]                   EXECUTING SELECTED TOOLS                   [/bold  magenta]")
        print("[bold magenta]" + "=" * 60 + "[/bold magenta]")

        step = 1

        for tool_name in self.plan:
            print("\n[dim]" + "-" * 60 + "[/dim]")
            print(f"[bold yellow]STEP {step}:[/bold yellow] Running [bold cyan]{tool_name}[/bold cyan]")
            print("[dim]" + "-" * 60 + "[/dim]")

            tool_func = TOOL_REGISTRY.get(tool_name)
            if tool_func:
                result = tool_func(self.goal)
                print("[bold green][OBSERVATION]:[/bold green]")
                print(f"[bright_white]{result.strip()}[/bright_white]")
                self.observation.append(result)
            else:
                print(f"[bold red][ERROR]:[/bold red] Tool {tool_name} not found in registry.")

            step += 1

    # Final response 
    def generate_final_plan(self):
        prompt = f"""
User Goal: {self.goal}
Collected Information: {self.observation}

- Generate a final response from the collected information and also generate a 90-day learning roadmap.
- If no information is gathered from the tools, return "No information was gathered."

Formatting constraints:
- Return plain text only.
- Do not use any Markdown formatting (no asterisks, hash tags, or bolding).
- Keep responses concise and brief (as short as possible).
"""

        response = gemini_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        print("\n[bold green]" + "=" * 60 + "[/bold green]")
        print("[bold  green]                      FINAL CAREER PLAN                       [/bold  green]")
        print("[bold green]" + "=" * 60 + "[/bold green]\n")

        return response.text

    # Run loop pattern
    def run(self):
        # Generate the tool sequence plan
        self.plan = self.create_plan()

        print("[bold cyan]GENERATED SEQUENCE:[/bold cyan]")
        if not self.plan:
            print("[italic red]  No specific tools were selected by the Planner Agent.[/italic red]\n")
        else:
            for index, tool in enumerate(self.plan):
                print(f"  [bold yellow][{index + 1}][/bold yellow] [bold cyan]{tool}[/bold cyan]")

        # Execute selected tools
        self.execute_plan()

        # Send the output of tool executions to Gemini and display the final output
        final_plan = self.generate_final_plan()
        print(f"[bold bright_white]{final_plan}[/bold bright_white]")


if __name__ == "__main__":
    goal = input("Enter your career goal: ")
    print()  # Add whitespace after user input
    career_coach = CareerCoachAgent(goal)
    career_coach.run()