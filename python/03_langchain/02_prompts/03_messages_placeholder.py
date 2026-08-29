import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
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

support_chat_prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful customer support assistant."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{user_query}"),
    ]
)

session_chat_history = []

# Safely read from file if it exists
if os.path.exists("chat_history.txt"):
    with open("chat_history.txt", "r") as chat_history_file:
        session_chat_history = [
            history_line.strip()
            for history_line in chat_history_file
            if history_line.strip()
        ]

formatted_chat_messages = support_chat_prompt_template.invoke(
    {
        "chat_history": session_chat_history,
        "user_query": "Where is my refund?",
    }
)

model_generation_response = llm_client.invoke(formatted_chat_messages)

print("=" * 70)
print(model_generation_response.content[0]["text"])  # type: ignore
print("=" * 70)
