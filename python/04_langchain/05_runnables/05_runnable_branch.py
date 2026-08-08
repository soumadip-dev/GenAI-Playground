# -----------------------------------------------------------------------------
# RunnableBranch Example using LangChain
#
# Workflow:
# 1. Accept a user query.
# 2. Determine whether the query is related to Mathematics, Science, or General
#    knowledge using RunnableBranch.
# 3. Route the query to the appropriate prompt.
# 4. Generate a response using the language model.
# -----------------------------------------------------------------------------
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableBranch, RunnableSequence
from langchain_groq import ChatGroq

load_dotenv()

chat_model = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.5,
)

string_output_parser = StrOutputParser()

# Prompt for mathematics-related questions
math_prompt = PromptTemplate.from_template("""
You are an expert Mathematics tutor.

Answer the following mathematics question clearly and accurately.

Question:
{query}

- Return the answer in plain text.
- Do not use Markdown or HTML.
""")

# Prompt for science-related questions
science_prompt = PromptTemplate.from_template("""
You are an expert Science tutor.

Answer the following science question clearly and accurately.

Question:
{query}

- Return the answer in plain text.
- Do not use Markdown or HTML.
""")

# Prompt for all other questions
general_prompt = PromptTemplate.from_template("""
You are a helpful AI assistant.

Answer the following question clearly and concisely.

Question:
{query}

- Return the answer in plain text.
- Do not use Markdown or HTML.
""")

query_router = RunnableBranch(
    (
        lambda x: "math" in x["query"].lower(),
        RunnableSequence(math_prompt, chat_model, string_output_parser),
    ),
    (
        lambda x: "science" in x["query"].lower(),
        RunnableSequence(science_prompt, chat_model, string_output_parser),
    ),
    RunnableSequence(general_prompt, chat_model, string_output_parser),
)

result = query_router.invoke(
    {
        "query": "What is the square root of 2?",
    }
)

print(result)


query_router.get_graph().print_ascii()
