# -----------------------------------------------------------------------------
# RunnablePassthrough Example using LangChain
#
# Workflow:
# 1. Generate a joke about a given topic.
# 2. Keep the generated joke unchanged using RunnablePassthrough.
# 3. Simultaneously generate an explanation of the joke.
# 4. Return both the original joke and its explanation.
# -----------------------------------------------------------------------------

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import (
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

# Prompt 1: Generate a joke
joke_generation_prompt = PromptTemplate.from_template("""
Write a funny and family-friendly joke about {topic}.

Requirements:
- Return only the joke.
- Use plain text.
- Do not use Markdown or HTML.
""")

# Prompt 2: Explain the generated joke
joke_explanation_prompt = PromptTemplate.from_template("""
Explain the following joke in simple and easy-to-understand language.

Joke:
{text}

Requirements:
- Return only the explanation.
- Use plain text.
- Do not use Markdown or HTML.
""")


string_output_parser = StrOutputParser()

# -----------------------------------------------------------------------------
# Joke Generation Chain
#
# Topic
#   ↓
# Joke Prompt
#   ↓
# Chat Model
#   ↓
# String Output Parser
# -----------------------------------------------------------------------------
joke_generation_chain = RunnableSequence(
    joke_generation_prompt,
    chat_model,
    string_output_parser,
)

# -----------------------------------------------------------------------------
# Parallel Chain
#
# The generated joke is sent to two branches:
#
#                 Generated Joke
#                      │
#         ┌────────────┴────────────┐
#         │                         │
# RunnablePassthrough      Joke Explanation Chain
#         │                         │
#         └────────────┬────────────┘
#                      │
#       {"joke", "explanation"}
# -----------------------------------------------------------------------------
joke_processing_chain = RunnableParallel(
    {
        # Returns the original joke without modification
        "joke": RunnablePassthrough(),
        # Generates an explanation of the joke
        "explanation": RunnableSequence(
            joke_explanation_prompt,
            chat_model,
            string_output_parser,
        ),
    }
)

# -----------------------------------------------------------------------------
# Final Chain
#
# Topic
#   ↓
# Joke Generation
#   ↓
# Parallel Processing
#   ├── Original Joke
#   └── Joke Explanation
# -----------------------------------------------------------------------------
final_chain = RunnableSequence(
    joke_generation_chain,
    joke_processing_chain,
)


result = final_chain.invoke(
    {
        "topic": "JavaScript",
    }
)


print("Joke:\n")
print(result["joke"])

print("\n" + "-" * 60 + "\n")

print("Explanation:\n")
print(result["explanation"])


final_chain.get_graph().print_ascii()
