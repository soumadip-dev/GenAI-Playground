# JSON Output Parser

import os

from dotenv import load_dotenv
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from rich import print

load_dotenv()

language_model = HuggingFaceEndpoint(
    model="Qwen/Qwen2.5-7B-Instruct",
    task="text-generation",
    huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
)

chat_model = ChatHuggingFace(llm=language_model)

# -----------------------------------------------------------------------------
# Workflow:
# 1. Ask the LLM to generate details of a fictional Indian person.
# 2. Force the response to follow a JSON format using JsonOutputParser.
# 3. Parse the JSON response into a Python dictionary.
# -----------------------------------------------------------------------------

json_output_parser = JsonOutputParser()

person_details_prompt = PromptTemplate(
    template="""
Give me the name, age, and city of a fictional Indian person.

{format_instructions}
""",
    input_variables=[],
    partial_variables={
        "format_instructions": json_output_parser.get_format_instructions()
    },
)

formatted_prompt = person_details_prompt.format()

# Send the prompt to the chat model
response = chat_model.invoke(formatted_prompt)

if not response or not response.content:
    print("[bold red]No response was received from the language model.[/bold red]")
else:
    # Convert the JSON string into a Python dictionary
    parsed_response = json_output_parser.parse(response.content)  # type: ignore

    # Display the parsed result
    print(parsed_response)
