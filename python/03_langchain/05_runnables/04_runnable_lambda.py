import os

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import (
    RunnableParallel,
    RunnableSequence,
    RunnablePassthrough,
    RunnableLambda,
)
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables from the .env file.
load_dotenv()


# Retrieve and validate the Gemini API key.
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable is missing.")


# Configure the Gemini chat model.
gemini_model_name = "gemini-3.5-flash-lite"

chat_model = ChatGoogleGenerativeAI(
    model=gemini_model_name,
    temperature=0.5,
    google_api_key=gemini_api_key,
)


# Convert the model's output into a plain Python string.
string_output_parser = StrOutputParser()


# ============================================================================================
# RunnableLambda
#
# Workflow:
# 1. Generate a short inspirational quote about the given topic.
# 2. Convert the model response into a plain string using StrOutputParser.
# 3. Process the generated quote through two parallel branches:
#    - RunnablePassthrough returns the original quote unchanged.
#    - RunnableLambda applies a Python function to calculate the word count.
# 4. Combine both results into a dictionary containing the quote and word count.
#
#                         ┌── RunnablePassthrough ── quote ───────────┐
# Topic ── Quote Chain ───┤                                           ├── {"quote", "word_count"}
#                         └── RunnableLambda ── word count ───────────┘
#
# ============================================================================================


# Prompt for generating the inspirational quote.
quote_generation_prompt = PromptTemplate.from_template("""
Write a short inspirational quote about {topic}.

Requirements:
- Return only the quote.
- Use plain text.
- Do not use Markdown or HTML.
- Keep the quote within one or two sentences.
""")


# Chain for generating the quote:
# PromptTemplate → Chat Model → StrOutputParser
quote_generation_chain = RunnableSequence(
    quote_generation_prompt,
    chat_model,
    string_output_parser,
)


# Python function for calculating the number of words in the quote.
def calculate_word_count(text: str) -> int:
    """Return the total number of words in the given text."""
    return len(text.split())


# Process the generated quote in parallel:
# - RunnablePassthrough returns the original quote unchanged.
# - RunnableLambda executes the Python function to calculate the word count.
quote_analysis_chain = RunnableParallel(
    {
        # Pass the generated quote to the output unchanged.
        "quote": RunnablePassthrough(),
        # Convert the Python function into a Runnable and calculate the word count.
        "word_count": RunnableLambda(calculate_word_count),
    }
)


# Complete workflow:
# Quote Generation Chain → Parallel Analysis Chain
final_chain = RunnableSequence(
    quote_generation_chain,
    quote_analysis_chain,
)


# Invoke the complete chain with the input topic.
response = final_chain.invoke({"topic": "Success"})


# Display the generated quote and its word count.
print("=" * 70)

print("Quote:\n")
print(response["quote"])

print("\n" + "-" * 60 + "\n")

print("Word Count:\n")
print(response["word_count"])

print("=" * 70)
