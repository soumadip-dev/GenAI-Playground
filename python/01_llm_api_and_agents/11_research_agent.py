# Research Agent: Plans, gathers evidence via tools, analyzes it,
# and produces career recommendations using the Gemini API.
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

# Header banner.
print(f"[bold cyan]{'=' * 60}[/bold cyan]")
print("[bold magenta]   Career Agent - Skills, Certifications, Projects & Salary   [/bold magenta]")
print(f"[bold cyan]{'=' * 60}[/bold cyan]\n")


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
- Entry Level: 8-12 LPA
- Mid Level: 15-25 LPA
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


# Registry mapping tool names to their implementation functions.
TOOL_REGISTRY = {
    "SKILL_TOOL": get_skills,
    "CERTIFICATION_TOOL": get_certificate,
    "PROJECT_TOOL": get_project_recommendations,
    "SALARY_TOOL": get_salary,
}


class ResearchAgent:
    def __init__(self, goal: str):
        self.goal = goal
        self.plan = []
        self.evidence = []

    # Ask the LLM to build a minimal research plan from the available tools.
    def create_research_plan(self):
        print("[bold cyan]Creating research plan...[/bold cyan]")

        prompt = f"""You are an expert AI Research Planner Agent responsible for breaking down a user's goal into an optimal, minimal research plan.

### USER GOAL
{self.goal}

### AVAILABLE TOOLS
SKILL_TOOL
CERTIFICATION_TOOL
PROJECT_TOOL
SALARY_TOOL

### YOUR TASK
Create the BEST research plan for this goal.

### RULES
1. Use only the tools that are actually required.
2. Do not include unnecessary tools.
3. Return one tool name per line.
4. Return ONLY tool names, nothing else.

### EXAMPLE OUTPUT
SKILL_TOOL
CERTIFICATION_TOOL
PROJECT_TOOL
SALARY_TOOL
"""
        response = gemini_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        plan = []
        text_content = response.text or ""
        for line in text_content.split("\n"):
            tool = line.strip()
            if tool in TOOL_REGISTRY:
                plan.append(tool)

        return plan

    # Run each planned tool and collect its output as evidence.
    def gather_evidence(self):
        print("[bold cyan]Gathering evidence...[/bold cyan]")

        for tool_name in self.plan:
            tool_func = TOOL_REGISTRY.get(tool_name)
            if tool_func:
                result = tool_func(self.goal)

                print("[dim]" + "-" * 60 + "[/dim]")
                print(f"[bold cyan]{tool_name}[/bold cyan]")
                print("[dim]" + "-" * 60 + "[/dim]")
                print(result)

                self.evidence.append(f"{tool_name}\n{result}")
            else:
                print(f"[bold red][ERROR][/bold red] Tool {tool_name} not found in registry.")

    # Ask the LLM to analyze the gathered evidence.
    def analyze_evidence(self):
        print("\n[bold cyan]" + "=" * 60 + "[/bold cyan]")
        print("[bold cyan]Analyzing evidence...[/bold cyan]")
        print("[bold cyan]" + "=" * 60 + "[/bold cyan]\n")

        prompt = f"""You are an AI Career Analyst.

### GOAL
{self.goal}

### EVIDENCE
{self.evidence}

### YOUR TASK
Based on the evidence above, generate:
1. Key findings
2. Opportunities
3. Challenges

Return the analysis as plain text without any markdown.(very short in 3 -4 sentences)
"""
        response = gemini_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        return response.text

    # Ask the LLM to turn the analysis into a final set of recommendations.
    def generate_recommendations(self, analysis):
        print("\n[bold green]" + "=" * 60 + "[/bold green]")
        print("[bold green]Generating recommendations...[/bold green]")
        print("[bold green]" + "=" * 60 + "[/bold green]\n")

        prompt = f"""### USER GOAL
{self.goal}

### ANALYSIS
{analysis}

### YOUR TASK
Based on the goal and analysis above, generate:
- Executive summary
- Recommendations
- Learning path
- Final verdict

Keep the reply short and reply in plain text format, not Markdown.(under 10 lines)
"""
        response = gemini_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        print("[bold green]Final Recommendation[/bold green]")
        print(response.text)

    # Run the full plan -> gather -> analyze -> recommend pipeline.
    def run(self):
        self.plan = self.create_research_plan()

        print("[bold cyan]GENERATED SEQUENCE:[/bold cyan]")
        if not self.plan:
            print("[italic red]  No specific tools were selected by the Planner Agent.[/italic red]\n")
        else:
            for index, tool in enumerate(self.plan):
                print(f"  [bold yellow][{index + 1}][/bold yellow] [bold cyan]{tool}[/bold cyan]")

        self.gather_evidence()

        analysis = self.analyze_evidence()
        print("[bold cyan]ANALYSIS:[/bold cyan]")
        print(analysis)

        self.generate_recommendations(analysis)


if __name__ == "__main__":
    goal = input("Enter your career goal: ")
    print()  # Add whitespace after user input
    career_coach = ResearchAgent(goal)
    career_coach.run()