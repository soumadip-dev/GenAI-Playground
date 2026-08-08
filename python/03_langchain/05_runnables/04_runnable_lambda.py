# -----------------------------------------------------------------------------
# RunnableLambda Example using LangChain
#
# Workflow:
# 1. Generate a short inspirational quote about a given topic.
# 2. Pass the generated quote directly to the final output.
# 3. Use RunnableLambda to calculate the word count of the quote.
# 4. Return both the original quote and its word count.
# -----------------------------------------------------------------------------

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import (
    RunnableLambda,
    RunnableParallel,
    RunnablePassthrough,
    RunnableSequence,
)
from langchain_groq import ChatGroq

load_dotenv()

chat_model = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.5,
)

# Prompt for quote generation
quote_generation_prompt = PromptTemplate.from_template("""
Write a short inspirational quote about {topic}.

Requirements:
- Return only the quote.
- Use plain text.
- Do not use Markdown or HTML.
- Keep the quote within one or two sentences.
""")


string_output_parser = StrOutputParser()

# -----------------------------------------------------------------------------
# Quote Generation Chain
#
# Flow:
# Topic
#   ↓
# Quote Prompt
#   ↓
# Chat Model
#   ↓
# String Output Parser
# -----------------------------------------------------------------------------
quote_generation_chain = RunnableSequence(
    quote_generation_prompt,
    chat_model,
    string_output_parser,
)


# -----------------------------------------------------------------------------
# Lambda Function
#
# Calculates the total number of words in the generated quote.
# -----------------------------------------------------------------------------
def calculate_word_count(text: str) -> int:
    """Return the total number of words in the given text."""
    return len(text.split())


# -----------------------------------------------------------------------------
# Parallel Chain
#
#              Generated Quote
#                     │
#        ┌────────────┴────────────┐
#        │                         │
# RunnablePassthrough       Word Counter
#        │                         │
#        └────────────┬────────────┘
#                     │
#      {"quote", "word_count"}
# -----------------------------------------------------------------------------
quote_analysis_chain = RunnableParallel(
    {
        # Pass the generated quote directly to the output
        "quote": RunnablePassthrough(),
        # Calculate the word count using RunnableLambda
        "word_count": RunnableLambda(calculate_word_count),
    }
)

# -----------------------------------------------------------------------------
# Final Chain
#
# Flow:
# Topic
#   ↓
# Quote Generation
#   ↓
# Parallel Execution
#   ├── Original Quote
#   └── Word Count
# -----------------------------------------------------------------------------
final_chain = RunnableSequence(
    quote_generation_chain,
    quote_analysis_chain,
)

result = final_chain.invoke(
    {
        "topic": "Success",
    }
)

print("Quote:\n")
print(result["quote"])

print("\n" + "-" * 60 + "\n")

print("Word Count:\n")
print(result["word_count"])


final_chain.get_graph().print_ascii()
