import os

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel
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
# Parallel Chain
# =========================================================
#                  ┌── Study Notes Chain ──┐
# Document ────────┤                       ├── Study Guide Chain ── Final
#                  └── Quiz Chain ─────────┘

# Create a prompt for generating study notes
study_notes_prompt = PromptTemplate.from_template("""
Read the following text and create concise, well-structured study notes.
Keep each point to one line.

Text:
{text}
""")


# Create a prompt for generating a quiz
quiz_generation_prompt = PromptTemplate.from_template("""
Read the following text and create a quiz with up to 5 questions.
Include a mix of:
- Multiple Choice
- True/False

Text:
{text}
""")


# Create a prompt for generating the final study guide
study_guide_prompt = PromptTemplate.from_template("""
Combine the following study notes and quiz into a concise study guide.
Keep the response within 15 lines.

Study Notes:
{notes}

Quiz:
{quiz}

Return plain text only. Do not use Markdown or HTML.
""")


# Create an output parser that converts the LLM response into a string
output_parser = StrOutputParser()


# Run study notes and quiz generation in parallel
parallel_chain = RunnableParallel(
    notes=study_notes_prompt | llm | output_parser,
    quiz=quiz_generation_prompt | llm | output_parser,
)


# Generate the final study guide from the parallel results
study_guide_chain = study_guide_prompt | llm | output_parser


# Combine the parallel and study guide chains
final_chain = parallel_chain | study_guide_chain

# The same chain can also be written as:
# final_chain = parallel_chain | study_guide_prompt | llm | output_parser


# Document text
document_text = """JavaScript is a programming language used to build interactive web applications.
It supports variables, functions, objects, arrays, and asynchronous programming.
JavaScript runs in browsers and can also run on servers using Node.js.
It is commonly used with frameworks and libraries such as React, Angular, and Vue.
"""

# Invoke the chain with the document text
response = final_chain.invoke({"text": document_text})


# Display the final study guide
print("=" * 70)
print(response)
print("=" * 70)
