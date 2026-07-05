from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.5,
)


chat_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful customer support agent",
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{query}"),
    ]
)

chat_history = []

with open("chat_history.txt") as f:
    chat_history.extend(f.readlines())

print(chat_history)

prompt = chat_template.invoke(
    {"chat_history": chat_history, "query": "Where is my refund"}
)

print(prompt)

response = llm.invoke(prompt)

print(f"🤖 : {response.content}")
