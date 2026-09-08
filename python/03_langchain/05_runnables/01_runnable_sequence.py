import os

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables from the .env file
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
# Runnable sequences
# =========================================================

# Create a prompt template for generating a joke about a given topic
joke_generation_prompt = PromptTemplate.from_template("""
Write a funny and family-friendly joke about {topic}.
Return only the joke in plain text.
""")

# Create a prompt template for explaining the generated joke
joke_explanation_prompt = PromptTemplate.from_template("""
Explain the following joke in simple and easy-to-understand language.

Joke:
{text}

Return only the explanation in plain text.
""")

# Create an output parser that converts the LLM response into a plain string
output_parser = StrOutputParser()

# -----------------------------------------------------------------------------
# Build the RunnableSequence
#
# Flow:
# Topic
#   ↓
# Joke Generation Prompt
#   ↓
# Chat Model
#   ↓
# String Output Parser
#   ↓
# Joke Explanation Prompt
#   ↓
# Chat Model
#   ↓
# String Output Parser
# -----------------------------------------------------------------------------
joke_explanation_chain = RunnableSequence(
    joke_generation_prompt,
    llm,
    output_parser,
    joke_explanation_prompt,
    llm,
    output_parser,
)

# Equivalent pipe syntax:
# joke_explanation_chain = (
#     joke_generation_prompt
#     | llm
#     | output_parser
#     | joke_explanation_prompt
#     | llm
#     | output_parser
# )

# Execute the chain
response = joke_explanation_chain.invoke(
    {
        "topic": "JavaScript",
    }
)

# Display output
print("=" * 70)
print(response)
print("=" * 70)
