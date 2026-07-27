from datetime import datetime
import os
import random

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


# Return the current local time.
def get_current_time(query=None):
    return datetime.now().strftime("%I:%M:%S %p")


# Evaluate a mathematical expression.
def calculate_expression(expression):
    try:
        return eval(expression)
    except Exception as error:
        return f"Invalid expression: {error}"


# Return a random motivational quote.
def get_motivational_quote(query=None):
    quotes = [
        "The only way to do great work is to love what you do.",
        "If you're not making mistakes, then you're not making decisions.",
        "You can't build a reputation on what you are going to do.",
        "Don't let yesterday take up too much of today.",
        "It's not about perfection. It's about progress.",
    ]

    return random.choice(quotes)


# Register all available tools.
TOOLS = {
    "TIME_TOOL": get_current_time,
    "CALCULATE_TOOL": calculate_expression,
    "MOTIVATIONAL_QUOTE_TOOL": get_motivational_quote,
}


# Select the most appropriate tool based on the user's query.
def select_tool(user_query):
    prompt = f"""
You are a tool-selection agent.

## Task
Choose the single most appropriate tool for the user's query.

## Available Tools

1. TIME_TOOL
   - Use for questions about the current time.

2. CALCULATE_TOOL
   - Use for mathematical expressions or arithmetic calculations.
   - mind it that the tool will use eval() to evaluate the expression so if something that is not executable using eval() then return "None"
   - example: 2 + 2 -> CALCULATE_TOOL
   but if calculate 2 + 2 * 3 then return "None" or what is 5*8 this is not executable using eval() so return "None" THIS PART IS VERY VERY IMPORTANT DONT MENTION THIS TYPE OF THINGS AS CALCULATE_TOOL ALWAYS RETURN "None"

3. MOTIVATIONAL_QUOTE_TOOL
   - Use when the user asks for motivation, encouragement, inspiration, or a quote.

## Rules

- Return only the tool name.
- Do not explain your reasoning.
- Do not include punctuation, Markdown, or extra text.
- If the user's query is not related to any available tool, return "None".
- Your response must be exactly one of:
  - TIME_TOOL
  - CALCULATE_TOOL
  - MOTIVATIONAL_QUOTE_TOOL
  - None

## Examples

User: What is the current time?
Assistant: TIME_TOOL

User: Can you tell me the time?
Assistant: TIME_TOOL

User: 2 + 2
Assistant: CALCULATE_TOOL

User: What is 15 * (9 + 1)?
Assistant: None

User: 9 / 8 * 65 * 78
Assistant: CALCULATE_TOOL

User: Motivate me.
Assistant: MOTIVATIONAL_QUOTE_TOOL

User: I'm feeling sad today.
Assistant: MOTIVATIONAL_QUOTE_TOOL

User: Give me an inspirational quote.
Assistant: MOTIVATIONAL_QUOTE_TOOL

User: What is AI?
Assistant: None

## User Query

User: {user_query}
"""

    response = gemini_client.interactions.create(
        model="gemini-3.5-flash-lite",
        input=prompt,
    )

    selected_tool = response.output_text.strip()  # type: ignore

    return selected_tool


# Handle queries that do not require any registered tool.
def generate_general_response(user_query):
    prompt = f"""
Solve the following query in 2-3 short lines.

Return the response in plain text without Markdown.

Query:
{user_query}
"""

    response = gemini_client.interactions.create(
        model="gemini-3.5-flash-lite",
        input=prompt,
    )

    assistant_response = response.output_text.strip()  # type: ignore

    return assistant_response


# Execute the selected tool or generate a general response.
def execute_tool(tool_name, user_query):
    tool = TOOLS.get(tool_name)

    if tool is None:
        return generate_general_response(user_query)

    return tool(user_query)


while True:
    user_query = input("\nYou: ")

    if user_query.lower() in ["bye", "exit", "quit"]:
        break

    selected_tool = select_tool(user_query)

    print(
        f"\n[bold cyan]Selected Tool:[/bold cyan] [bold green]{selected_tool}[/bold green]"
    )

    response = execute_tool(selected_tool, user_query)

    print(
        f"\n[bold magenta]Assistant:[/bold magenta] {response}"
    )