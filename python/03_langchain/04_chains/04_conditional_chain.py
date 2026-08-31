import os
from typing import Literal

from dotenv import load_dotenv
from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableBranch, RunnableLambda
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field

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
# Conditional Chain
# =========================================================

# Feedback
#     ↓
# Sentiment Classification Prompt
#     ↓
# Gemini LLM
#     ↓
# Pydantic Output Parser
#     ↓
# FeedbackSentiment
#     ↓
# Runnable Branch
#     ├── Positive → Positive Response Prompt → Gemini LLM
#     └── Negative → Negative Response Prompt → Gemini LLM
#                              ↓
#                       String Output Parser
#                              ↓
#                       Final Response


# Define the expected structure of the feedback sentiment
class FeedbackSentiment(BaseModel):
    """Represents the sentiment classification of user feedback."""

    sentiment: Literal["positive", "negative"] = Field(
        description="The sentiment of the feedback."
    )


# Create a parser for the structured sentiment output
sentiment_output_parser = PydanticOutputParser(pydantic_object=FeedbackSentiment)


# Create a parser that converts the final LLM response into a plain string
string_output_parser = StrOutputParser()


# Get formatting instructions required by the Pydantic output parser
sentiment_format_instructions = sentiment_output_parser.get_format_instructions()


# Create a prompt for classifying the sentiment of user feedback
sentiment_classification_prompt = PromptTemplate(
    template="""Classify the sentiment of the following user feedback as either positive or negative.

Feedback:
{feedback}

{format_instructions}
""",
    input_variables=["feedback"],
    partial_variables={"format_instructions": sentiment_format_instructions},
)


# Create the chain that classifies feedback sentiment
sentiment_classifier_chain = (
    sentiment_classification_prompt | llm | sentiment_output_parser
)


# Create a prompt for generating a response to positive feedback
positive_feedback_prompt = PromptTemplate.from_template(
    """You are a customer support assistant.

Write a short and appropriate response to this positive feedback:

{feedback}
"""
)


# Create a prompt for generating a response to negative feedback
negative_feedback_prompt = PromptTemplate.from_template(
    """You are a customer support assistant.

Write a short and appropriate response to this negative feedback:

{feedback}
"""
)


# Create a conditional branch based on the classified sentiment
feedback_response_branch = RunnableBranch(
    (
        lambda feedback_sentiment: feedback_sentiment.sentiment == "positive",
        positive_feedback_prompt | llm | string_output_parser,
    ),
    (
        lambda feedback_sentiment: feedback_sentiment.sentiment == "negative",
        negative_feedback_prompt | llm | string_output_parser,
    ),
    RunnableLambda(lambda _: "Unable to determine the feedback sentiment."),
)


# Classify the feedback and then generate an appropriate response
feedback_response_chain = sentiment_classifier_chain | feedback_response_branch


# User feedback
user_feedback = "This is an exquisite phone."


# Invoke the chain with the user's feedback
response = feedback_response_chain.invoke({"feedback": user_feedback})


# Display the final response
print("=" * 70)
print(response)
print("=" * 70)
