from dotenv import load_dotenv
from google import genai
from google.genai import types
from rich import print

import os

# Load environment variables from the .env file.
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

print("[bold cyan]" + "=" * 60 + "[/bold cyan]")
print("[bold green]Gemini Career Assistant[/bold green]")
print("[bold cyan]" + "=" * 60 + "[/bold cyan]")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is not configured.")

# Initialize the Gemini client.
gemini_client = genai.Client(api_key=API_KEY)


# Return the required skills for a given career role.
def get_skills(role: str) -> dict:
    """
    Retrieve the core skills required for a career role.

    Args:
        role: The target career role.

    Returns:
        A dictionary containing the role and its required skills.
    """
    return {
        "role": role,
        "skills": [
            "Python",
            "Machine Learning",
            "Data Science",
            "Web Development",
        ],
    }


# Return recommended certifications for a given career role.
def get_certificate(role: str) -> dict:
    """
    Retrieve recommended certifications for a career role.

    Args:
        role: The target career role.

    Returns:
        A dictionary containing the role and recommended certifications.
    """
    return {
        "role": role,
        "certificates": [
            "AI-102",
            "AZ-104",
            "DP-300",
            "AWS Cloud Practitioner",
            "Google GenAI",
        ],
    }


# Return an estimated salary range for a given career role.
def get_salary(role: str) -> dict:
    """
    Retrieve the estimated salary range for a career role.

    Args:
        role: The target career role.

    Returns:
        A dictionary containing the role and estimated salary range.
    """
    return {
        "role": role,
        "salary_range": "$50,000 - $100,000",
    }


# Register all available tools.
TOOLS = [
    get_skills,
    get_certificate,
    get_salary,
]

user_query = input("Enter your query: ")

response = gemini_client.models.generate_content(
    model="gemini-2.5-flash",
    contents=user_query,
    config=types.GenerateContentConfig(
        tools=TOOLS,
    ),
)

print("\n[bold magenta]Assistant:[/bold magenta]")
print(response.text)