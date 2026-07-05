import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.load import load

load_dotenv()


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict this in production.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.5,
)


class InputRequest(BaseModel):
    input: str


# Static prompt
@app.post("/summarize")
async def generate_summary(request: InputRequest):
    if not request.input.strip():
        return {
            "success": False,
            "message": "Input is required.",
            "data": None,
        }

    response = llm.invoke(request.input)

    return {
        "success": True,
        "message": "Summary generated successfully.",
        "data": {"summary": response.content},
    }


# You can define the prompt template here or store it in a separate JSON file.
# To store it in another file, use template.save("template.json") inside prompt_generator.py.

# template = PromptTemplate(
#     template="""
# Please summarize the research paper titled "{paper_input}" with the following specifications:
# Explanation Style: {style_input}
# Explanation Length: {length_input}
# 1. Mathematical Details:
#    - Include relevant mathematical equations if present in the paper.
#    - Explain the mathematical concepts using simple, intuitive code snippets where applicable.
# 2. Analogies:
#    - Use relatable analogies to simplify complex ideas.
# If certain information is not available in the paper, respond with: "Insufficient information available" instead of guessing.
# Ensure the summary is clear, accurate, and aligned with the provided style and length.
# """,
#     input_variables=["paper_input", "style_input", "length_input"],
#     validate_template=True,
# )

# After running prompt_generator.py, it will generate the prompt
# and save it as template.json.
# Now load the prompt from template.json using load().
with open("template.json", "r", encoding="utf-8") as f:
    template_dict = json.load(f)
template = load(template_dict)


class SummaryRequest(BaseModel):
    paperInput: str
    styleInput: str
    lengthInput: str


# Dynamic prompt
@app.post("/paper-summary/prompt")
async def generate_paper_summary_from_prompt(request: SummaryRequest):

    if (
        not request.paperInput.strip()
        or not request.styleInput.strip()
        or not request.lengthInput.strip()
    ):
        return {
            "success": False,
            "message": "All inputs are required.",
            "data": None,
        }

    # Generate the prompt using the template.
    formatted_prompt = template.invoke(
        {
            "paper_input": request.paperInput,
            "style_input": request.styleInput,
            "length_input": request.lengthInput,
        }
    )

    # Invoke the LLM.
    response = llm.invoke(formatted_prompt)

    return {
        "success": True,
        "message": "Research paper summary generated successfully.",
        "data": {"summary": response.content},
    }


# Dynamic prompt with langchain_chain
@app.post("/paper-summary/chain")
async def generate_paper_summary_with_chain(request: SummaryRequest):

    if (
        not request.paperInput.strip()
        or not request.styleInput.strip()
        or not request.lengthInput.strip()
    ):
        return {
            "success": False,
            "message": "All inputs are required.",
            "data": None,
        }

    chain = template | llm

    response = chain.invoke(
        {
            "paper_input": request.paperInput,
            "style_input": request.styleInput,
            "length_input": request.lengthInput,
        }
    )

    return {
        "success": True,
        "message": "Research paper summary generated successfully.",
        "data": {"summary": response.content},
    }
