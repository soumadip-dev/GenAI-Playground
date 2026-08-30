import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

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

# Create an output parser that converts the LLM response into a plain string
output_parser = StrOutputParser()


# Create the LCEL chain
chain = llm | output_parser


# User prompt
user_prompt = (
    "I know JavaScript, React, Node.js and MongoDB. "
    "Recommend a suitable career path."
)


# Invoke the chain and get the parsed response
parsed_response = chain.invoke(user_prompt)


# Display output
print("=" * 70)
print(parsed_response)
print("=" * 70)
