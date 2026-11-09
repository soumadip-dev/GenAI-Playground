import os
from dotenv import load_dotenv
from google import genai
from rich import print
from importlib import import_module

# Load environment variables from the .env file.
load_dotenv()

# Import ResearchAgent from the numbered file
research_agent_module = import_module('11_research_agent')
ResearchAgent = research_agent_module.ResearchAgent

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is not configured.")

gemini_client = genai.Client(api_key=API_KEY)


class ReflectionAgent:
    """
    Reflection Agent
    Responsibilities:
      1. Review the first draft
      2. Identify weaknesses
      3. Suggest improvements
      4. Generate improved reports
    """

    def __init__(self, model_name: str = "gemini-3.5-flash-lite"):
        self.model_name = model_name

    def review(self, draft: str) -> str | None:
        """Evaluates the draft report and returns concise, structured critique."""
        print("\n[bold red]" + "=" * 60 + "[/bold red]")
        print("[bold red]Reviewing draft...[/bold red]")
        print("[bold red]" + "=" * 60 + "[/bold red]\n")

        prompt = f"""You are a Senior AI Content Reviewer. Evaluate the following career report and provide a structured critique.

CAREER REPORT TO REVIEW:
{draft}

EVALUATION CRITERIA:
1. Accuracy
2. Completeness
3. Clarity
4. Practicality & Actionability
5. Missing Information

OUTPUT RULES:
- Direct Critique Only: Do NOT rewrite or regenerate the report.
- Brevity: Keep feedback concise, punchy, and as brief as possible.
- Plain Text Output: Do NOT use Markdown formatting (no asterisks, hash tags, or markdown tables). Use plain text lists or simple indentation only.

FEEDBACK FORMAT:
Strengths:
- [Point 1]
- [Point 2]

Weaknesses:
- [Point 1]
- [Point 2]

Suggested Actionable Improvements:
- [Point 1]
- [Point 2]
"""
        response = gemini_client.models.generate_content(
            model=self.model_name,
            contents=prompt,
        )

        feedback_text = response.text
        print("[bold red]Feedback:[/bold red]")
        print(feedback_text)

        return feedback_text

    def improve_draft(self, draft: str, feedback: str) -> str | None:
        """Rewrites and improves the draft based on reviewer feedback."""
        print("\n[bold magenta]" + "=" * 60 + "[/bold magenta]")
        print("[bold magenta]Improving draft...[/bold magenta]")
        print("[bold magenta]" + "=" * 60 + "[/bold magenta]\n")

        prompt = f"""You are an expert AI Career Consultant. 

ORIGINAL CAREER REPORT:
{draft}

REVIEWER FEEDBACK:
{feedback}

TASK:
Rewrite and substantially improve the career report by addressing the feedback.

REQUIREMENTS:
- Address every reviewer comment in full.
- Retain all accurate and strong elements from the original draft.
- Expand weak sections with clear detail.
- Fill in missing information identified in the feedback.
- Provide highly practical recommendations and an actionable step-by-step roadmap.
- Always give response in very short and txt format not markdown.
"""
        response = gemini_client.models.generate_content(
            model=self.model_name,
            contents=prompt,
        )

        improved_text = response.text
        print("[bold magenta]Improved Report:[/bold magenta]")
        print(improved_text)

        return improved_text

    def reflect(self, draft: str) -> str | None:
        """Orchestrates the draft -> review -> improve workflow."""
        feedback = self.review(draft)
        if feedback:
            final_improved_report = self.improve_draft(draft, feedback)
        else:
            final_improved_report = draft

        print("\n[bold green]" + "=" * 60 + "[/bold green]")
        print("[bold green]FINAL REFLECTED REPORT:[/bold green]")
        print("[bold green]" + "=" * 60 + "[/bold green]\n")

        print(f"[bold white]{final_improved_report}[/bold white]")

        return final_improved_report


def main():
    """Main execution function that orchestrates Research Agent -> Reflection Agent workflow."""
    # Header banner.
    print(f"[bold cyan]{'=' * 60}[/bold cyan]")
    print("[bold magenta]   Career Agent - Skills, Certifications, Projects & Salary   [/bold magenta]")
    print(f"[bold cyan]{'=' * 60}[/bold cyan]\n")

    goal = input("Enter your career goal: ")
    print()  # Add whitespace after user input

    # Step 1: Run Research Agent to generate analysis and recommendations
    print("[bold yellow]STEP 1: RESEARCH PHASE[/bold yellow]\n")
    research_agent = ResearchAgent(goal)
    analysis, recommendations = research_agent.run()

    # Step 2: Apply Reflection Agent on the recommendations from Research Agent
    print("\n[bold yellow]STEP 2: REFLECTION PHASE[/bold yellow]\n")
    reflection_agent = ReflectionAgent()

    if recommendations:
        reflection_agent.reflect(recommendations)
    else:
        print("[bold red]No recommendations generated to reflect upon.[/bold red]")


if __name__ == "__main__":
    main()