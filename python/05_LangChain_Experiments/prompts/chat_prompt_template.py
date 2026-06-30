from langchain_core.prompts import ChatPromptTemplate
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
            "You are a helpful {domain} expert who can explain things in simple terms one line.",
        ),
        ("human", "Explain in simple terms, What is {topic}"),
    ]
)

chain = chat_template | llm

response = chain.invoke({"domain": "cricket", "topic": "the Duckworth-Lewis method"})

print(response.content)
