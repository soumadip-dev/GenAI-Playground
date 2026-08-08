from dotenv import load_dotenv
from google import genai
import os
from rich import print

# Load environment variables
load_dotenv()


# Initialize Gemini client
gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Generate response
gemini_response = gemini_client.interactions.create(
    model="gemini-3.5-flash-lite",
    input="Explain how AI works in a few words",
)

# Print assistant reply
assistant_reply = gemini_response.output_text  # type: ignore


print(assistant_reply)
