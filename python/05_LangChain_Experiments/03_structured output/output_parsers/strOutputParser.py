# String Output Parser

import os

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

load_dotenv()

language_model = HuggingFaceEndpoint(
    model="Qwen/Qwen2.5-7B-Instruct",
    task="text-generation",
    huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
)

chat_model = ChatHuggingFace(llm=language_model)

# -----------------------------------------------------------------------------
# Workflow:
# 1. Generate a detailed report on a given topic.
# 2. Convert the generated report into a one-line summary.
# 3. Parse the LLM responses as plain text using StrOutputParser.
# -----------------------------------------------------------------------------


# Prompt Templates

# Prompt 1: Generate a detailed report about the given topic
detailed_report_prompt = PromptTemplate.from_template(
    "Write a detailed report about the following topic: {topic}",
)

# Prompt 2: Summarize the generated report in one line
summary_prompt = PromptTemplate.from_template(
    "Write a one-line summary of the following report:\n\n{detailed_report}"
)

# Output Parser: Converts the model's response into a plain Python string.
string_output_parser = StrOutputParser()


# -----------------------------------------------------------------------------
# Build the LangChain Pipeline
#
# Flow:
# Topic
#   ↓
# Detailed Report Prompt
#   ↓
# Chat Model
#   ↓
# String Output Parser
#   ↓
# Summary Prompt
#   ↓
# Chat Model
#   ↓
# String Output Parser
# -----------------------------------------------------------------------------
report_and_summary_chain = (
    detailed_report_prompt.pipe(chat_model)
    .pipe(string_output_parser)
    .pipe(summary_prompt)
    .pipe(chat_model)
    .pipe(string_output_parser)
)


result = report_and_summary_chain.invoke(
    {
        "topic": "Black hole",
    }
)

print(result)
