from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Initialize Groq client
groq_client = Groq()

# Generate response
chat_response = groq_client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {"role": "user", "content": "Hey, I am Soumadip Majila! Nice to meet you!"}
    ],
)

# Print assistant reply
assistant_reply = chat_response.choices[0].message.content
print(assistant_reply)
