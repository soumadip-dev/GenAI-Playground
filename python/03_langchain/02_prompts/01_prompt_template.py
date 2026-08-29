import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables from .env file
load_dotenv()

# Verify API key existence
google_api_key = os.getenv("GEMINI_API_KEY")
llm_model_name = "gemini-3.5-flash-lite"

if not google_api_key:
    raise ValueError("GEMINI_API_KEY environment variable is missing in .env file.")

llm_client = ChatGoogleGenerativeAI(
    model=llm_model_name,
    temperature=0.5,
    google_api_key=google_api_key,
)

template = PromptTemplate.from_template(
    "Explain the concept of {concept} in simple terms for a {target_audience}."
)

# Format the prompt dynamically
formatted_prompt = template.invoke(
    {"concept": "Recursion", "target_audience": "beginner developer"}
)

response = llm_client.invoke(formatted_prompt)

print("=" * 70)
print(response.content[0]["text"])  # type: ignore
print("=" * 70)
