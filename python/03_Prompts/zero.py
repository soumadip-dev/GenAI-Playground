from dotenv import load_dotenv
from groq import Groq

load_dotenv()

groq_client = Groq()

# Zero-shot prompting:
# The model is given a direct instruction or task without any prior examples.
SYSTEM_PROMPT = """
You are Venom, a coding assistant.
Answer only coding-related questions.
If the user asks anything unrelated to coding, respond only with:
'Sorry, I can only help with coding-related questions.'
Do not add any extra explanation.
"""


chat_response = groq_client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": "Hey, can you write a JavaScript program to print 'Hello, World!'?",
        },
    ],
)

assistant_reply = chat_response.choices[0].message.content
print(assistant_reply)
