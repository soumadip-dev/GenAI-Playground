import json
import os
from datetime import datetime

from dotenv import load_dotenv
from groq import Groq
from tavily import TavilyClient
from cachetools import TTLCache

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
tavily_api_key = os.getenv("TAVILY_API_KEY")

if not groq_api_key or not tavily_api_key:
    raise ValueError("Missing GROQ_API_KEY or TAVILY_API_KEY")

client = Groq(api_key=groq_api_key)
tavily_client = TavilyClient(api_key=tavily_api_key)

# In-memory conversation storage (24 hours TTL)
storage = TTLCache(maxsize=1000, ttl=60 * 60 * 24)


def web_search(query: str) -> str:
    response = tavily_client.search(query, max_results=3)

    results = [
        result["content"]
        for result in response.get("results", [])
        if result.get("content")
    ]

    return "\n".join(results) if results else "No search results found."


tools = [
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the internet for the latest information.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query to perform.",
                    }
                },
                "required": ["query"],
            },
        },
    }
]


def generate(user_message: str, thread_id: str) -> str | None:

    current_dt = datetime.now().astimezone().strftime("%a, %d %b %Y %I:%M:%S %p %Z")

    base_messages = [
        {
            "role": "system",
            "content": f"""You are a smart personal assistant.

Your responsibilities:
- If you know the answer to a question, answer it directly in plain English.
- If a question requires real-time, local, or up-to-date information, or if you don't know the answer, use the available tools to find it.
- Decide when to rely on your own knowledge and when to use a tool.
- Do not mention tools unless necessary.
- Keep your responses concise and to the point. Avoid unnecessary explanations or irrelevant details. Always respond in plain text.

Available tool:

web_search(query: string) -> Use this tool to search the internet for current, local, up-to-date, or unknown information.

Current date and time: {current_dt}
""",
        }
    ]

    # Retrieve existing history or initialize a new conversation
    messages = storage.get(thread_id, base_messages.copy())

    # Append current user message
    messages.append({"role": "user", "content": user_message})

    # Tool-calling loop
    while True:
        chat_completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            temperature=0,
            messages=messages,
            tools=tools,
            tool_choice="auto",
        )

        assistant_message = chat_completion.choices[0].message

        # Final response
        if not assistant_message.tool_calls:
            messages.append({"role": "assistant", "content": assistant_message.content})

            # Save updated conversation history
            storage[thread_id] = messages

            return assistant_message.content

        # Append assistant tool-call message
        messages.append(assistant_message)

        # Execute requested tools
        for tool_call in assistant_message.tool_calls:
            function_name = tool_call.function.name
            print(f"Tool Called: {function_name}")

            try:
                function_params = json.loads(tool_call.function.arguments or "{}")
            except json.JSONDecodeError:
                function_params = {}

            if function_name == "web_search":
                query = function_params.get("query")

                if not isinstance(query, str) or not query.strip():
                    tool_result = "Invalid or missing search query."
                else:
                    tool_result = web_search(query)
            else:
                tool_result = f"Unknown tool: {function_name}"

            # Append tool result
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": tool_result,
                }
            )
