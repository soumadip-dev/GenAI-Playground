from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Initialize the Groq client
groq_client = Groq()

# Generate a response
chat_response = groq_client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {
            "role": "user",
            "content": "Hey, can you help me solve (a + b)²?",
        },
        {
            "role": "system",
            "content": (
                "You are an expert in mathematics. "
                "Answer only questions related to mathematics. "
                "If the question is not related to mathematics, "
                "respond only with 'I don't know'."
            ),
        },
    ],
)

# Print the assistant's reply
assistant_reply = chat_response.choices[0].message.content
print(assistant_reply)
