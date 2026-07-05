# Pydantic Output Parser


import os

from dotenv import load_dotenv
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from pydantic import BaseModel, Field
from rich import print

load_dotenv()

language_model = HuggingFaceEndpoint(
    model="Qwen/Qwen2.5-7B-Instruct",
    task="text-generation",
    huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
)

chat_model = ChatHuggingFace(llm=language_model)


class Person(BaseModel):
    """Represents structured information about a fictional person."""

    name: str = Field(description="Full name of the person.")
    age: int = Field(description="Age of the person in years.")
    gender: str = Field(description="Gender of the person.")
    occupation: str = Field(description="Current occupation or profession.")
    city: str = Field(description="City where the person lives.")


person_output_parser = PydanticOutputParser(pydantic_object=Person)


person_details_prompt = PromptTemplate(
    template="""
Give me the details of a fictional {nationality} person.

{format_instructions}
""",
    input_variables=["nationality"],
    partial_variables={
        "format_instructions": person_output_parser.get_format_instructions()
    },
)

formatted_prompt = person_details_prompt.format(nationality="Indian")


response = chat_model.invoke(formatted_prompt)

if not response or not response.content:
    print("[bold red]No response was received from the language model.[/bold red]")
else:
    # Parse and validate the response as a Pydantic object
    parsed_person = person_output_parser.parse(response.content)  # type: ignore

    # Display the validated object
    print(parsed_person)
