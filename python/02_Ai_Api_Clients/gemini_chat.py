from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Initialize Gemini client
gemini_client = genai.Client()

# Generate response
gemini_response = gemini_client.interactions.create(
    model="gemini-2.5-flash-lite",
    input="Explain how AI works in a few words",
)

# Print assistant reply
assistant_reply = gemini_response.output_text
print(assistant_reply)
