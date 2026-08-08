# Structured Output Parser

import os

from dotenv import load_dotenv
from langchain_classic.output_parsers import StructuredOutputParser, ResponseSchema
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

response_schemas = [
    ResponseSchema(
        name="fact_1",
        description="The first fact about the given topic.",
        type="string",
    ),
    ResponseSchema(
        name="fact_2",
        description="The second fact about the given topic.",
        type="string",
    ),
    ResponseSchema(
        name="fact_3",
        description="The third fact about the given topic.",
        type="string",
    ),
]

structured_output_parser = StructuredOutputParser.from_response_schemas(
    response_schemas
)


facts_prompt = PromptTemplate.from_template("""
Give three facts about {topic}.

{format_instructions}
""").partial(format_instructions=structured_output_parser.get_format_instructions())

formatted_prompt = facts_prompt.format(topic="India")

response = chat_model.invoke(formatted_prompt)

if not response or not response.content:
    print("[bold red]No response was received from the language model.[/bold red]")
else:
    # Convert the structured response into a Python dictionary
    parsed_response = structured_output_parser.parse(response.content)  # type: ignore

    # Display the parsed output
    print(parsed_response)
