import os
from typing import Literal

from dotenv import load_dotenv
from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableBranch, RunnableLambda, RunnableSequence
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field

# Load environment variables from the .env file.
load_dotenv()


# Retrieve and validate the Gemini API key.
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable is missing in .env file.")


# Configure the Gemini chat model.
gemini_model_name = "gemini-3.5-flash-lite"

chat_model = ChatGoogleGenerativeAI(
    model=gemini_model_name,
    temperature=0.5,
    google_api_key=gemini_api_key,
)


# =================================================================================
# RunnableBranch
#
# Workflow:
# 1. Accept a user question.
# 2. Classify the question as either "math" or "general".
# 3. Parse the classification into a Pydantic model.
# 4. Use RunnableBranch to choose the appropriate response.
# 5. Return a message indicating the type of question asked.
#
#                         ┌── Math ──────── "You asked a math question."
# Question ── Classify ───┤
#                         └── General ───── "You asked a general question."
#
# =================================================================================


# Pydantic model for the question classification result.
class QuestionClassification(BaseModel):
    classification: Literal["math", "general"] = Field(
        description="The category of the question: 'math' for mathematics-related questions or 'general' for all other questions."
    )


# Parser for the structured classification output.
classification_output_parser = PydanticOutputParser(
    pydantic_object=QuestionClassification
)


# Get formatting instructions required by the Pydantic output parser.
classification_format_instructions = (
    classification_output_parser.get_format_instructions()
)


# Prompt for classifying the user's question.
classification_prompt = PromptTemplate.from_template("""
Classify the following question into one of these categories:

- "math" — if the question is related to mathematics.
- "general" — for all other questions.

Question:
{query}

{format_instructions}
""").partial(format_instructions=classification_format_instructions)


# Chain for classifying the question:
# PromptTemplate → Chat Model → PydanticOutputParser
classification_chain = RunnableSequence(
    classification_prompt,
    chat_model,
    classification_output_parser,
)


# Route the classification to the appropriate response.
question_router = RunnableBranch(
    (
        lambda classification: classification.classification == "math",
        RunnableLambda(lambda _: "You asked a math question."),
    ),
    (
        lambda classification: classification.classification == "general",
        RunnableLambda(lambda _: "You asked a general question."),
    ),
    RunnableLambda(lambda _: "Unable to classify the question."),
)


# Complete workflow:
# Question → Classification Chain → RunnableBranch
final_chain = RunnableSequence(
    classification_chain,
    question_router,
)


# Invoke the chain with a question.
response = final_chain.invoke(
    {
        "query": "What is the square root of 2?",
    }
)


# Display the result.
print("=" * 70)
print(response)
print("=" * 70)
