import json
import os
from dotenv import load_dotenv
from groq import Groq
from tavily import TavilyClient
from datetime import datetime, timezone

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
tavily_api_key = os.getenv("TAVILY_API_KEY")

if not groq_api_key or not tavily_api_key:
    raise ValueError("Missing GROQ_API_KEY or TAVILY_API_KEY")

client = Groq(api_key=groq_api_key)
tavily_client = TavilyClient(api_key=tavily_api_key)


def web_search(query: str) -> str:
    response = tavily_client.search(query, max_results=3)

    results = [result["content"] for result in response.get("results", [])]

    return "\n".join(results) if results else "No search results found."


def main():
    messages = [
        {
            "role": "system",
            "content": f"""You are a smart personal assistant who answers questions
            to the point and in one line.

            You have access to the following tool:
            1. web_search(query: string) -> Search the latest information
            on the internet.

            Use this tool whenever you need current information.
            current datetime: {datetime.now().astimezone().strftime('%a, %d %b %Y %I:%M:%S %p %Z')}
            """,
        }
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

    while True:
        question = input("\nYou: ").strip()

        # Exit condition
        if question.lower() in ["exit", "quit", "bye"]:
            print("Assistant: Goodbye!")
            break

        if not question:
            continue

        messages.append({"role": "user", "content": question})

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
                print(f"Assistant: {assistant_message.content}")

                messages.append(
                    {"role": "assistant", "content": assistant_message.content}
                )

                break

            # Append assistant tool-call message
            messages.append(assistant_message)

            # Execute requested tools
            for tool_call in assistant_message.tool_calls:

                function_name = tool_call.function.name

                function_params = json.loads(tool_call.function.arguments)

                print(f"Tool Called: {function_name}")

                if function_name == "web_search":
                    tool_result = web_search(**function_params)
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


if __name__ == "__main__":
    main()
