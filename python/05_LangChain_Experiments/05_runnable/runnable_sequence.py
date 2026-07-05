# -----------------------------------------------------------------------------
# RunnableSequence Example using LangChain
#
# Workflow:
# 1. Generate a joke about a given topic.
# 2. Parse the joke as plain text.
# 3. Explain the generated joke.
# 4. Parse and display the explanation.
# -----------------------------------------------------------------------------

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
from langchain_groq import ChatGroq

# Load environment variables from the .env file
load_dotenv()

chat_model = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.5,
)

# Prompt 1: Generate a joke about the given topic
joke_generation_prompt = PromptTemplate.from_template("""
Write a funny and family-friendly joke about {topic}.
Return only the joke in plain text.
""")

# Prompt 2: Explain the generated joke
joke_explanation_prompt = PromptTemplate.from_template("""
Explain the following joke in simple and easy-to-understand language.

Joke:
{text}

Return only the explanation in plain text.
""")

string_output_parser = StrOutputParser()

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
    chat_model,
    string_output_parser,
    joke_explanation_prompt,
    chat_model,
    string_output_parser,
)

# Equivalent pipe syntax:
# joke_explanation_chain = (
#     joke_generation_prompt
#     | chat_model
#     | string_output_parser
#     | joke_explanation_prompt
#     | chat_model
#     | string_output_parser
# )

# Execute the chain
result = joke_explanation_chain.invoke(
    {
        "topic": "JavaScript",
    }
)

print(result)
