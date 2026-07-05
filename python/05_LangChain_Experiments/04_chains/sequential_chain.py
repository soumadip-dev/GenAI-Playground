# Sequential Chain Example using LangChain


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

# Prompt Templates

# Prompt 1: Generate a short report on the given topic
report_generation_prompt = PromptTemplate.from_template(
    "Generate a 5–6 line report on the topic: {topic}. Return the response in plain text format.",
)

# Prompt 2: Summarize the generated report in one line
report_summary_prompt = PromptTemplate.from_template(
    "Write a one-line summary of the following report:\n\n{report}",
)


string_output_parser = StrOutputParser()

report_summary_chain = (
    report_generation_prompt
    | chat_model
    | string_output_parser
    | report_summary_prompt
    | chat_model
    | string_output_parser
)


result = report_summary_chain.invoke(
    {
        "topic": "Artificial Intelligence",
    }
)

# Display the final one-line summary
print(result)

# Visualize the chain structure
report_summary_chain.get_graph().print_ascii()
