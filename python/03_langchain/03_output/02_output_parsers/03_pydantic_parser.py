import os
from typing import Literal

from dotenv import load_dotenv
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
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


# Define the expected output structure
class CareerRecommendation(BaseModel):
    role: str = Field(description="Recommended career role")

    level: Literal["Beginner", "Intermediate", "Advanced"] = Field(
        description="Current skill level"
    )

    skills: list[str] = Field(description="Skills to learn")


# Create an output parser that converts the LLM response
# into a CareerRecommendation Pydantic object
output_parser = PydanticOutputParser(pydantic_object=CareerRecommendation)


# Get the format instructions for the output parser
format_instructions = output_parser.get_format_instructions()


# Create the prompt template
prompt_template = PromptTemplate(
    template="""
I know JavaScript, React, Node.js and MongoDB.
Recommend a suitable career path.

{format_instructions}
""",
    input_variables=[],
    partial_variables={"format_instructions": format_instructions},
)


# Create the LCEL chain
chain = prompt_template | llm | output_parser


# Invoke the chain and get the parsed response
career_recommendation = chain.invoke({})


# Display output
print("=" * 70)
print(career_recommendation)
print("=" * 70)
