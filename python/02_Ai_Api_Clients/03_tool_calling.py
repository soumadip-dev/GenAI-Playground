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


# Return the current local time
def get_current_time():
    return datetime.now().strftime("%I:%M:%S %p")


# Evaluate a mathematical expression
def calculate_expression(expression):
    try:
        return eval(expression)
    except Exception as ex:
        return f"Invalid expression: {ex}"


# Return a random motivational quote
def get_motivational_quote():
    quotes = [
        "The only way to do great work is to love what you do.",
        "If you're not making mistakes, then you're not making decisions.",
        "You can't build a reputation on what you are going to do.",
        "Don't let yesterday take up too much of today.",
        "It's not about perfection. It's about progress.",
    ]
    return random.choice(quotes)


# Initialize the Gemini client
gemini_client = genai.Client(api_key=API_KEY)


# Route the user query to the appropriate tool
def route_tool(query):
    query = query.lower()

    if "time" in query or "date" in query or "current time" in query:
        return "time"

    elif (
        "quote" in query
        or "motivational" in query
        or "inspirational" in query
        or "motivation" in query
    ):
        return "quote"

    elif "calculator" in query or "math" in query or "calculate" in query:
        return "calculator"

    return "gemini"


while True:
    user_input = input("You: ")

    if user_input.lower() in ["bye", "exit", "quit"]:
        break

    selected_tool = route_tool(user_input)

    match selected_tool:
        case "time":
            current_time = get_current_time()
            print(f"\nGemini: Current time is {current_time}")

        case "quote":
            quote = get_motivational_quote()
            print(f"\nGemini: {quote}")

        case "calculator":
            expression = user_input.replace("calculate", "").strip()
            calculation_result = calculate_expression(expression)
            print(f"\nGemini: {calculation_result}")

        case "gemini":
            # Generate a response using Gemini
            response = gemini_client.interactions.create(
                model="gemini-3.5-flash-lite",
                input=user_input,
            )

            assistant_response = response.output_text  # type: ignore
            print(f"\nGemini: {assistant_response}")
