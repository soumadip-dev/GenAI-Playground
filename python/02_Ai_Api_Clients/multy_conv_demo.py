from dotenv import load_dotenv
from google import genai
import os
from rich import print

# Load environment variables from the .env file
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is not configured.")

# Initialize the Gemini client
gemini_client = genai.Client(api_key=API_KEY)

# Store conversation history
chat_history = []

SYSTEM_PROMPT = """
You are a friendly AI assistant.

Rules:
1. Be helpful.
2. Be professional.
3. Keep responses clean and concise.
4. Do not say you are an AI.
5. Reply in plain English without Markdown.
6. Remember previous conversation context.
"""

while True:
    user_input = input("You: ")

    if user_input.lower() in ["bye", "exit", "quit"]:
        break

    chat_history.append(f"User: {user_input}")

    conversation_prompt = SYSTEM_PROMPT + "\n"
    conversation_prompt += "\n".join(chat_history)

    # Generate a response from Gemini
    response = gemini_client.interactions.create(
        model="gemini-3.5-flash-lite",
        input=conversation_prompt,
    )

    assistant_response = response.output_text  # type: ignore

    print(f"\nGemini: {assistant_response}")

    chat_history.append(f"Assistant: {assistant_response}")
