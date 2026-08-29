import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables from .env file
load_dotenv()

# Verify API key existence
google_api_key = os.getenv("GEMINI_API_KEY")
llm_model_name = "gemini-3.5-flash-lite"

if not google_api_key:
    raise ValueError("GEMINI_API_KEY environment variable is missing in .env file.")

llm_client = ChatGoogleGenerativeAI(
    model=llm_model_name,
    temperature=0.5,
    google_api_key=google_api_key,
)

system_prompt_content = (
    "You are a senior software engineer with 15+ years of experience.\n"
    "Your responsibilities:\n"
    "- Write clean, optimized, production-ready code\n"
    "- Explain your solution in simple language\n"
    "- Mention time and space complexity where applicable\n"
    "- Suggest industry best practices and standard design patterns.\n"
    "Target Explanation Difficulty Level: {difficulty}"
)

coding_assistant_prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt_content),
        ("human", "{user_query}"),
    ]
)

print("AI Coding Assistant Initialized.\n" + "=" * 50)

user_coding_query = input("\nEnter your question: ").strip()

target_difficulty_level = input(
    "Enter target difficulty (e.g., beginner, intermediate, advanced): "
).strip()
if not target_difficulty_level:
    target_difficulty_level = "intermediate"

print("\nGenerating response...\n")

# Combine all template variables into a single dictionary mapping
formatted_chat_messages = coding_assistant_prompt_template.invoke(
    {
        "user_query": user_coding_query,
        "difficulty": target_difficulty_level,
    }
)

# Pass the formatted prompt directly to the model
model_generation_response = llm_client.invoke(formatted_chat_messages)

print("=" * 70)
print(model_generation_response.content[0]["text"])  # type: ignore
print("=" * 70)
