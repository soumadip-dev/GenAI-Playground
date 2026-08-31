import os

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables from .env file
load_dotenv()


# Get and verify the Gemini API key
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable is missing in .env file.")


# LLM configuration
gemini_model_name = "gemini-3.5-flash-lite"


# Initialize the Gemini LLM
llm = ChatGoogleGenerativeAI(
    model=gemini_model_name,
    temperature=0.5,
    google_api_key=gemini_api_key,
)

# =========================================================
# Sequential chain
# =========================================================

# Create a prompt template for generating a report
report_prompt_template = PromptTemplate.from_template(
    "Generate a 5–6 line report on the topic: {topic}. Return the response in plain text format.",
)


# Create a prompt template for summarizing the generated report
summary_prompt_template = PromptTemplate.from_template(
    "Write a one-line summary of the following report:\n\n{report}",
)


# Create an output parser that converts the LLM response into a plain string
output_parser = StrOutputParser()


# Create a sequential LCEL chain:
# Report Prompt → LLM → Output Parser
# → Summary Prompt → LLM → Output Parser
report_summary_chain = (
    report_prompt_template
    | llm
    | output_parser
    | summary_prompt_template
    | llm
    | output_parser
)


# Get the topic from the user
topic = input("Enter a topic: ")


# Invoke the chain with the user-provided topic
response = report_summary_chain.invoke({"topic": topic})


# Display output
print("=" * 70)
print(response)
print("=" * 70)
