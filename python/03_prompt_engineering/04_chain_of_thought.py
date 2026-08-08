from dotenv import load_dotenv
from groq import Groq
import json

# Load environment variables
load_dotenv()

# Initialize the Groq client
groq_client = Groq()

# Chain-of-Thought Prompting (Planning Pattern)
# The model is instructed to solve the problem step by step by
# generating a plan before producing the final answer.
SYSTEM_PROMPT = """
You are Venom, an expert AI assistant that solves user queries using a planning process.

Follow these steps:

1. START
   - Read and understand the user's request.

2. PLAN
   - Break the task into logical steps.
   - You may generate multiple PLAN steps if necessary.

3. OUTPUT
   - Once the plan is complete, provide the final answer.

Rules:
- Return only valid JSON.
- Perform only one step at a time.
- Always follow this sequence:
  START → PLAN (one or more times) → OUTPUT

Output format:

{
  "step": "START" | "PLAN" | "OUTPUT",
  "content": string
}

Examples:

Example 1

Q: What is 25 × 12 + 50 × 2?

A:
{"step":"START","content":"The user wants to solve the mathematical expression 25 × 12 + 50 × 2."}

{"step":"PLAN","content":"This is a mathematics problem."}

{"step":"PLAN","content":"Apply the order of operations (BODMAS/PEMDAS)."}

{"step":"PLAN","content":"Calculate 25 × 12 = 300."}

{"step":"PLAN","content":"Calculate 50 × 2 = 100."}

{"step":"PLAN","content":"Add the results: 300 + 100 = 400."}

{"step":"OUTPUT","content":"400"}

------------------------------------------------

Example 2

Q: Write a JavaScript program to print 'Hello, World!'

A:
{"step":"START","content":"The user wants a JavaScript program that prints 'Hello, World!'."}

{"step":"PLAN","content":"Identify the requested programming language."}

{"step":"PLAN","content":"Use JavaScript's console.log() function."}

{"step":"PLAN","content":"Generate a valid JavaScript program."}

{"step":"OUTPUT","content":"```javascript\\nconsole.log('Hello, World!');\\n```"}

------------------------------------------------

Example 3

Q: What is the capital of Japan?

A:
{"step":"START","content":"The user is asking for the capital of Japan."}

{"step":"PLAN","content":"Recall the capital city of Japan."}

{"step":"PLAN","content":"Provide a concise and accurate answer."}

{"step":"OUTPUT","content":"The capital of Japan is Tokyo."}
"""

print("\n" * 4)

# Initialize the conversation history
message_history = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT,
    }
]

# Get the user's query
user_query = input("👉 ")
message_history.append(
    {
        "role": "user",
        "content": user_query,
    }
)

while True:
    # Generate the next response
    chat_response = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        response_format={"type": "json_object"},
        messages=message_history,  # type: ignore
    )

    assistant_reply = chat_response.choices[0].message.content

    # Save the assistant's response
    message_history.append(
        {
            "role": "assistant",
            "content": assistant_reply,  # type: ignore
        }
    )

    # Parse the JSON response
    parsed_response = json.loads(assistant_reply)  # type: ignore

    # If the model returns a single object, convert it to a list
    if isinstance(parsed_response, dict):
        parsed_response = [parsed_response]

    # Process each step
    for response in parsed_response:
        step = response.get("step")
        content = response.get("content")

        if step == "START":
            print(f"🔥 START  : {content}")

        elif step == "PLAN":
            print(f"🧠 PLAN   : {content}")

        elif step == "OUTPUT":
            print(f"🤖 OUTPUT : {content}")
            exit()

        else:
            print("❌ Invalid response from the model.")
            exit()
