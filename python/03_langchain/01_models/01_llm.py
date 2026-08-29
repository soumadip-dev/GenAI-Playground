import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAI

# Load environment variables from .env file
load_dotenv()

# Verify API key existence
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable is missing in .env file.")

# Initialize the Gemini model
llm = GoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
)

# Invoke the model with a prompt
prompt = "What is the capital of France?"
response = llm.invoke(prompt)

# Output
print("=" * 70)
print("MODEL RESPONSE:")
print(response)
print("=" * 70)
