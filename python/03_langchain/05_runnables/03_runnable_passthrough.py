import os

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import (
    RunnableParallel,
    RunnablePassthrough,
    RunnableSequence,
)
from langchain_google_genai import ChatGoogleGenerativeAI

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

# ============================================================================================
# Runnable Passthrough
#
# Workflow:
# 1. Generate a joke about the given topic.
# 2. Convert the model response into a plain string using StrOutputParser.
# 3. Pass the generated joke unchanged through the "joke" branch.
# 4. Send the same joke to the "explanation" branch to generate an explanation.
# 5. Combine both branches into a dictionary containing the joke and explanation.
#
#                       ┌── RunnablePassthrough ── joke ──────────┐
# Topic ── Joke Chain ──┤                                         ├── {"joke", "explanation"}
#                       └── Explanation Chain ── explanation ─────┘
#
# ============================================================================================

# Prompt for generating the joke.
joke_generation_prompt = PromptTemplate.from_template("""
Write a funny and family-friendly joke about {topic}.

Requirements:
- Return only the joke.
- Use plain text.
- Do not use Markdown or HTML.
""")

# Prompt for explaining the generated joke.
joke_explanation_prompt = PromptTemplate.from_template("""
Explain the following joke in simple and easy-to-understand language.

Joke:
{text}

Requirements:
- Return only the explanation.
- Use plain text.
- Do not use Markdown or HTML.
""")

# Convert the model's output into a plain Python string.
string_output_parser = StrOutputParser()


# Chain for generating the joke:
# PromptTemplate → Chat Model → StrOutputParser
joke_generation_chain = RunnableSequence(
    joke_generation_prompt,
    chat_model,
    string_output_parser,
)


# Process the generated joke in parallel:
# - RunnablePassthrough returns the original joke unchanged.
# - The explanation chain generates an explanation of the joke.
joke_processing_chain = RunnableParallel(
    {
        # Pass the generated joke to the output unchanged.
        "joke": RunnablePassthrough(),
        # Generate an explanation of the generated joke.
        "explanation": RunnableSequence(
            joke_explanation_prompt,
            chat_model,
            string_output_parser,
        ),
    }
)


# Complete workflow:
# Joke Generation Chain → Parallel Processing Chain
final_chain = RunnableSequence(
    joke_generation_chain,
    joke_processing_chain,
)


# Invoke the complete chain with the input topic.
result = final_chain.invoke(
    {
        "topic": "JavaScript",
    }
)

# Display the generated joke and its explanation.
print("=" * 70)

print("Joke:\n")
print(result["joke"])

print("\n" + "-" * 60 + "\n")

print("Explanation:\n")
print(result["explanation"])
print("=" * 70)
