import json
import os
from datetime import datetime
from dotenv import load_dotenv
from groq import Groq
from tavily import TavilyClient

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
tavily_api_key = os.getenv("TAVILY_API_KEY")

if not groq_api_key or not tavily_api_key:
    raise ValueError("Missing GROQ_API_KEY or TAVILY_API_KEY")

client = Groq(api_key=groq_api_key)
tavily_client = TavilyClient(api_key=tavily_api_key)


def web_search(query: str) -> str:
    response = tavily_client.search(query, max_results=3)
    results = [
        result["content"]
        for result in response.get("results", [])
        if result.get("content")
    ]
    return "\n".join(results) if results else "No search results found."


def generate(user_message: str) -> str | None:
    current_dt = datetime.now().astimezone().strftime("%a, %d %b %Y %I:%M:%S %p %Z")

    messages = [
        {
            "role": "system",
            "content": f"""You are a smart personal assistant who answers questions
to the point and in one line.

You have access to the following tool:
1. web_search(query: string) -> Search the latest information on the internet.

Use this tool whenever you need current information.
current datetime: {current_dt}""",
        },
        {"role": "user", "content": user_message},
    ]

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

            # Send tool result back to LLM
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": tool_result,
                }
            )