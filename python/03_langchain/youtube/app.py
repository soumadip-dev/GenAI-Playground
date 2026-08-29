import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")

# Create Generative model
model = ChatGoogleGenerativeAI(
    model=MODEL_NAME,
    temperature=0.5,
    google_api_key=GEMINI_API_KEY,
)


response = model.invoke("What is the capital of France?")


print("=" * 60)
print(response.content[0]["text"])  # type: ignore
print("=" * 60)
