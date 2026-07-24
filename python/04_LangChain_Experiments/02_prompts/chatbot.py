from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()


def create_chat_model():
    return ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.5,
    )


def start_chat():
    chat_model = create_chat_model()
    conversation_history = []

    while True:
        user_message = input("You: ")
        if user_message.lower() == "exit":
            break
        conversation_history.append(HumanMessage(content=user_message))
        ai_response = chat_model.invoke(conversation_history)
        conversation_history.append(AIMessage(content=ai_response.content))
        print("AI:", ai_response.content)

    print("\nConversation History:")
    print(conversation_history)


start_chat()
