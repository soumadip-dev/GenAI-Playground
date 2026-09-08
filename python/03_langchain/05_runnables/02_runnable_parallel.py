import os

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnableSequence
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables from the .env file
load_dotenv()


# Get the Gemini API key from the environment
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable is missing.")


# LLM configuration
gemini_model_name = "gemini-3.5-flash-lite"


# Initialize the Gemini LLM
llm = ChatGoogleGenerativeAI(
    model=gemini_model_name,
    temperature=0.5,
    google_api_key=gemini_api_key,
)


# Create a string output parser
string_output_parser = StrOutputParser()


# =========================================================
# Runnable Parallel
# =========================================================
#                  ┌── Generate Tweet Chain ────────────┐
# Topic ───────────┤                                    ├── {"tweet", "linkedin"}
#                  └── Generate LinkedIn Chain ─────────┘


# Prompt for tweet generation
tweet_generation_prompt = PromptTemplate.from_template("""
Generate a single tweet about {topic}.

Requirements:
- Return only the tweet.
- Use plain text.
- Do not use Markdown or HTML.
""")


# Prompt for LinkedIn post generation
linkedin_post_prompt = PromptTemplate.from_template("""
Generate a professional LinkedIn post about {topic}.

Requirements:
- Return only the post.
- Use plain text.
- Do not use Markdown or HTML.
""")


# Run both generation chains in parallel
social_media_generation_chain = RunnableParallel(
    {
        "tweet": RunnableSequence(
            tweet_generation_prompt,
            llm,
            string_output_parser,
        ),
        "linkedin": RunnableSequence(
            linkedin_post_prompt,
            llm,
            string_output_parser,
        ),
    }
)


# Invoke the parallel chain with the input topic
result = social_media_generation_chain.invoke(
    {
        "topic": "LangChain",
    }
)


# Display the generated results
print("=" * 70)
print("Tweet:\n")
print(result["tweet"])

print("\n" + "-" * 60 + "\n")

print("LinkedIn Post:\n")
print(result["linkedin"])
print("=" * 70)
