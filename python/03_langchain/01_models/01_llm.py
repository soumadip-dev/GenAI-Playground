import os

from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAI

# Load environment variables from .env file.
load_dotenv()

# Retrieve the Gemini API key.
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Verify that the API key exists.
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable is missing.")

# Initialize the Gemini LLM.
llm = GoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    google_api_key=gemini_api_key,
)

# Invoke the model with a text prompt.
prompt = "What is the capital of France?"
response = llm.invoke(prompt)

# Display the model response.
print("=" * 70)
print("MODEL RESPONSE:")
print(response)
print("=" * 70)
