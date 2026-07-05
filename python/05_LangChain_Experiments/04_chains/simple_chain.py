# Simple chain

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from rich import print

load_dotenv()

chat_model = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.5,
)

facts_prompt = PromptTemplate(
    template=(
        "Generate five interesting facts about {topic} in plain text format. "
        "Each fact should be a single sentence."
    ),
    input_variables=["topic"],
)

string_output_parser = StrOutputParser()

facts_generation_chain = facts_prompt | chat_model | string_output_parser

result = facts_generation_chain.invoke(
    {
        "topic": "Bangali",
    }
)

print(result)

# Visualize the chain structure
facts_generation_chain.get_graph().print_ascii()
