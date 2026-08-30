import os
from typing import Literal, Optional

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field

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
class CareerRecommendation(BaseModel):
    role: str = Field(description="Recommended career role")

    level: Literal["Beginner", "Intermediate", "Advanced"] = Field(
        description="Current skill level"
    )

    skills: Optional[list[str]] = Field(description="Skills to learn")


# Create LLM with structured output
structured_llm = llm.with_structured_output(CareerRecommendation)  # type: ignore


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
