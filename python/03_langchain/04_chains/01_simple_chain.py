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
# Simple Chain
# =========================================================

# Create a reusable prompt template with a dynamic topic variable
prompt_template = PromptTemplate.from_template(
    "Generate 5 interesting facts about {topic} in 5 lines."
)

# Create an output parser that converts the LLM response into a plain string
output_parser = StrOutputParser()


# Create the LCEL chain:
# Prompt Template → LLM → Output Parser
career_facts_chain = prompt_template | llm | output_parser


# Get the topic from the user
topic = input("Enter a topic: ")


# Invoke the chain with the user-provided topic
response = career_facts_chain.invoke({"topic": topic})


# Display output
print("=" * 70)
print(response)
print("=" * 70)


# Display the visual graph of the LCEL chain => pip install grandalf
career_facts_chain.get_graph().print_ascii()
