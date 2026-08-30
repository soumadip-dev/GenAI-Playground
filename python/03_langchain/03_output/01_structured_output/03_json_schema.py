import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables from .env file
load_dotenv()


# Get and verify API key
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable is missing in .env file.")


# LLM configuration
gemini_model_name = "gemini-3.5-flash-lite"


# Initialize LLM
llm = ChatGoogleGenerativeAI(
    model=gemini_model_name,
    temperature=0.5,
    google_api_key=gemini_api_key,
)

# =========================================================
# =========================================================


# Define structured output schema
career_recommendation_schema = {
    "title": "CareerRecommendation",  # Name of the structured output
    "type": "object",  # The output must be a JSON object
    "properties": {  # Define the fields and their expected data types
        "role": {
            "type": "string",
            "description": "Recommended career role",
        },
        "level": {
            "type": "string",
            "enum": ["Beginner", "Intermediate", "Advanced"],
            "description": "Current skill level",
        },
        "skills": {
            "type": "array",
            "items": {
                "type": "string",
            },
            "description": "Skills to learn",
        },
    },
    "required": ["role", "level"],  # Fields that must be present in the output
}

# Create LLM with structured output
structured_llm = llm.with_structured_output(career_recommendation_schema)


# User prompt
user_prompt = (
    "I know JavaScript, React, Node.js and MongoDB. "
    "Recommend a suitable career path."
)


# Generate structured response
career_recommendation = structured_llm.invoke(user_prompt)


# Display output
print("=" * 70)
print(career_recommendation)
print("=" * 70)
