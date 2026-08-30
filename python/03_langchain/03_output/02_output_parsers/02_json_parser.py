import os

from dotenv import load_dotenv
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
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

# Create an output parser that converts the LLM response into a Python dictionary
output_parser = JsonOutputParser()

# Get the format instructions for the output parser
format_instructions = output_parser.get_format_instructions()

# Create the prompt template
prompt_template = PromptTemplate(
    template="""
Give me a random person from world history. Include their name, age,
country, profession, and one sentence about them as a brief biography.

{format_instructions}
""",
    input_variables=[],
    partial_variables={"format_instructions": format_instructions},
)

# Create the LCEL chain
chain = prompt_template | llm | output_parser


# Invoke the chain and get the parsed response
parsed_response = chain.invoke({})


# Display output
print("=" * 70)
print(parsed_response)
print("=" * 70)
