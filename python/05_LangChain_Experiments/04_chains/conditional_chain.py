# -----------------------------------------------------------------------------
# Conditional Chain Example using LangChain
#
# Workflow:
# 1. Classify the user's feedback as Positive or Negative.
# 2. Parse the classification into a Pydantic object.
# 3. Route the execution to the appropriate response generation chain.
# 4. Generate a polite two-line response based on the detected sentiment.
# -----------------------------------------------------------------------------

from typing import Literal

from dotenv import load_dotenv
from langchain_core.output_parsers import (
    PydanticOutputParser,
    StrOutputParser,
)
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableBranch, RunnableLambda
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field

load_dotenv()

chat_model = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.5,
)


# Parses normal text responses
string_output_parser = StrOutputParser()


# Pydantic model for sentiment classification
class FeedbackSentiment(BaseModel):
    """Represents the sentiment of user feedback."""

    sentiment: Literal["positive", "negative"] = Field(
        description="The sentiment of the feedback."
    )


# Parses and validates the sentiment classification
sentiment_output_parser = PydanticOutputParser(pydantic_object=FeedbackSentiment)

# Prompt 1: Sentiment Classification
sentiment_classification_prompt = PromptTemplate(
    template="""
You are a sentiment analysis assistant.

Analyze the following user feedback and determine whether its sentiment is
either **positive** or **negative**.

Feedback:
{feedback_text}

{format_instructions}
""",
    input_variables=["feedback_text"],
    partial_variables={
        "format_instructions": sentiment_output_parser.get_format_instructions()
    },
)
# -----------------------------------------------------------------------------
# Chain to classify the sentiment
# -----------------------------------------------------------------------------
sentiment_classifier_chain = (
    sentiment_classification_prompt | chat_model | sentiment_output_parser
)

# Prompt 2: Response for Positive Feedback
positive_feedback_prompt = PromptTemplate(
    template="""
You are a customer support assistant.

Write an appropriate response to the following positive feedback.

Feedback:
{feedback}

Requirements:
- Be polite and respectful.
- Thank the user for their feedback.
- Respond in plain text only.
- Do not use Markdown or HTML.
- Keep the response within two lines.
""",
    input_variables=["feedback"],
)

# Prompt 3: Response for Negative Feedback
negative_feedback_prompt = PromptTemplate(
    template="""
You are a customer support assistant.

Write an appropriate response to the following negative feedback.

Feedback:
{feedback}

Requirements:
- Be polite and respectful.
- Thank the user for their feedback.
- Respond in plain text only.
- Do not use Markdown or HTML.
- Keep the response within two lines.
""",
    input_variables=["feedback"],
)

# -----------------------------------------------------------------------------
# Conditional Branch
#
# If sentiment == positive  → Positive response chain
# If sentiment == negative  → Negative response chain
# Otherwise                 → Default message
# -----------------------------------------------------------------------------
feedback_response_branch = RunnableBranch(
    (
        lambda sentiment: sentiment.sentiment == "positive",
        positive_feedback_prompt | chat_model | string_output_parser,
    ),
    (
        lambda sentiment: sentiment.sentiment == "negative",
        negative_feedback_prompt | chat_model | string_output_parser,
    ),
    RunnableLambda(lambda _: "User did not provide valid feedback."),
)

# -----------------------------------------------------------------------------
# Final Chain
#
# Feedback
#     ↓
# Sentiment Classification
#     ↓
# Runnable Branch
#     ├── Positive Response
#     └── Negative Response
# -----------------------------------------------------------------------------
feedback_response_chain = sentiment_classifier_chain | feedback_response_branch


result = feedback_response_chain.invoke(
    {
        "feedback_text": "This is an exquisite phone.",
    }
)

print(result)

# Visualize the chain structure
feedback_response_chain.get_graph().print_ascii()
