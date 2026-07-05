# -----------------------------------------------------------------------------
# RunnableParallel Example using LangChain
#
# Workflow:
# 1. Accept a topic as input.
# 2. Generate a tweet about the topic using the Groq model.
# 3. Generate a LinkedIn post about the same topic using the Gemini model.
# 4. Execute both tasks in parallel.
# 5. Display both generated outputs.
# -----------------------------------------------------------------------------

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnableSequence
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq

# Load environment variables from the .env file
load_dotenv()


# Model used for tweet generation
groq_chat_model = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.5,
)

# Model used for LinkedIn post generation
gemini_chat_model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    temperature=0.5,
)

string_output_parser = StrOutputParser()


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

# -----------------------------------------------------------------------------
# Parallel Chain
#
#                Topic
#                  │
#        ┌─────────┴─────────┐
#        │                   │
#   Generate Tweet     Generate LinkedIn Post
#      (Groq)                (Gemini)
#        │                   │
#        └─────────┬─────────┘
#                  │
#      {"tweet", "linkedin"}
# -----------------------------------------------------------------------------
social_media_generation_chain = RunnableParallel(
    {
        "tweet": RunnableSequence(
            tweet_generation_prompt,
            groq_chat_model,
            string_output_parser,
        ),
        "linkedin": RunnableSequence(
            linkedin_post_prompt,
            gemini_chat_model,
            string_output_parser,
        ),
    }
)

result = social_media_generation_chain.invoke(
    {
        "topic": "LangChain",
    }
)


print("Tweet:\n")
print(result["tweet"])

print("\n" + "-" * 60 + "\n")

print("LinkedIn Post:\n")
print(result["linkedin"])
