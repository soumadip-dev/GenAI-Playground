import os

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables from .env file.
load_dotenv()

# Retrieve the Gemini API key.
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Set the model name.
llm_model_name = "gemini-3.5-flash-lite"

# Verify that the API key exists.
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable is missing.")

# Initialize the Gemini chat model.
model = ChatGoogleGenerativeAI(
    model=llm_model_name,
    temperature=0.5,
    google_api_key=gemini_api_key,
)


# Create structured conversational messages.
messages = [
    SystemMessage(content="You are a helpful assistant that provides concise answers."),
    HumanMessage(content="What is the capital of France?"),
]

# Invoke the chat model with the message sequence.
response = model.invoke(messages)


# Output
print("=" * 70)
print("CHAT MODEL RESPONSE:")
print(response.content)
print("=" * 70)
