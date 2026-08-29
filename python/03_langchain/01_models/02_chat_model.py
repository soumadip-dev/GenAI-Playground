import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables from .env file
load_dotenv()

# Retrieve configurations from environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")

# Verify API key existence
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is missing in .env file.")

# Initialize the ChatGoogleGenerativeAI model
model = ChatGoogleGenerativeAI(
    model=MODEL_NAME,
    temperature=0.5,
    google_api_key=GEMINI_API_KEY,
)


# Send query to the model
prompt = "What is the capital of France?"
response = model.invoke(prompt)


# Output
print("=" * 70)
print("MODEL RESPONSE:")
print(response.content[0]["text"])  # type: ignore
print("=" * 70)
