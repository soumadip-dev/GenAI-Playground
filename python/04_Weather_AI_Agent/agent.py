from dotenv import load_dotenv

from groq import Groq

from groq.types.chat import ChatCompletionMessageParam

import json

import requests

from pydantic import BaseModel, Field

from typing import Literal, Optional

# Load environment variables

load_dotenv()


# Initialize the Groq client

groq_client = Groq()


class WeatherData(BaseModel):

    step: Literal["START", "PLAN", "TOOL", "OBSERVE", "OUTPUT"]

    # Optional fields

    content: Optional[str] = Field(
        None, description="The optional string content of the step"
    )

    tool: Optional[str] = Field(None, description="The optional ID of the tool called")

    input: Optional[str] = Field(None, description="The optional input to the tool")

    output: Optional[str] = Field(None, description="The optional output of the tool")


def get_weather(city: str) -> str:
    """Fetch weather information for a given city."""

    try:

        url = f"https://wttr.in/{city.lower()}?format=%C+%t"

        response = requests.get(url, timeout=5)

        if response.status_code == 200:

            return f"The weather in {city} is {response.text}"

        else:

            return f"I don't know the weather in that city."

    except requests.RequestException as e:

        return f"Error fetching weather: {str(e)}"


available_tools = {
    "get_weather": get_weather,
}


SYSTEM_PROMPT = """

You are Nimbus, an expert weather assistant that provides weather information for a given city.

Follow these steps:

1. START

   - Read and understand the user's request.

2. PLAN

   - Break the task into logical steps.

   - You may generate multiple PLAN steps if necessary.

3. TOOL (if needed)

   - Call a tool if required from the list of available tools.

4. OBSERVE (if tool was called)

   - Wait for and record the tool output.

5. OUTPUT

   - Once the plan is complete, provide the final answer.

 

Rules:

- Return exactly one JSON object representing the next step only. Never return multiple steps or an array.

- Perform only one step at a time.

- Always follow this sequence:

  START → PLAN (one or more times) → TOOL (if needed) → OBSERVE (if tool called) → [return to PLAN or OUTPUT]

- When using a tool, include the tool name and parameters.

 

Output format:

For regular steps:

{

  "step": "START" | "PLAN" | "OUTPUT",

  "content": string

}

 

For tool calls:

{

  "step": "TOOL",

  "tool": string,

  "input": string

}

 

For tool results:

{

  "step": "OBSERVE",

  "tool": string,

  "output": string

}

 

Available tools:

- get_weather(city: str): Takes a city name as input and returns the weather information of that city.

 

Examples:

Example 1: Simple Question (No Tool Needed)

Q: What is the capital of France?

A:

{"step":"START","content":"The user is asking for the capital of France."}

{"step":"PLAN","content":"Recall the capital city of France from knowledge."}

{"step":"PLAN","content":"Provide the answer."}

{"step":"OUTPUT","content":"The capital of France is Paris."}

 

Example 2: Weather Query (Tool Required)

Q: What is the weather in New York?

A:

{"step":"START","content":"The user wants to know the weather in New York."}

{"step":"PLAN","content":"This requires real-time weather information."}

{"step":"PLAN","content":"I need to use the get_weather tool with 'New York' as the city parameter."}

{"step":"TOOL","tool":"get_weather","input":"New York"}

{"step":"OBSERVE","tool":"get_weather","output":"The weather in New York is Clear +30°C"}

{"step":"PLAN","content":"Great, I got the weather data for New York."}

{"step":"OUTPUT","content":"The current weather in New York is Clear and 30°C."}

 

Example 3: Weather Comparison (Multiple Tool Calls)

Q: Is it warmer in Paris or Berlin today?

A:

{"step":"START","content":"The user wants to compare temperatures between Paris and Berlin."}

{"step":"PLAN","content":"I need to fetch weather data for both cities to compare."}

{"step":"PLAN","content":"First, I will get the weather in Paris using the get_weather tool."}

{"step":"TOOL","tool":"get_weather","input":"Paris"}

{"step":"OBSERVE","tool":"get_weather","output":"The weather in Paris is Clear +16°C"}

{"step":"PLAN","content":"Next, I will get the weather in Berlin using the get_weather tool."}

{"step":"TOOL","tool":"get_weather","input":"Berlin"}

{"step":"OBSERVE","tool":"get_weather","output":"The weather in Berlin is Partly Cloudy +15°C"}

{"step":"PLAN","content":"Compare the temperatures from both cities."}

{"step":"OUTPUT","content":"Paris is warmer than Berlin today. Paris is at 16°C with clear skies, while Berlin is at 15°C with partly cloudy conditions. The temperature difference is minimal, but Paris has better weather conditions overall."}

 

Example 4: Misspelled City (Fuzzy Matching)

Q: What is the weather in delhiii?

A:

{"step":"START","content":"The user wants to know the weather in delhiii, which appears to be a misspelled city name."}

{"step":"PLAN","content":"The city name 'delhiii' is likely a misspelling. I should check for similar city names."}

{"step":"PLAN","content":"The closest match to 'delhiii' is 'Delhi'. This is a valid city name."}

{"step":"PLAN","content":"I will use the corrected city name 'Delhi' to fetch the weather."}

{"step":"TOOL","tool":"get_weather","input":"Delhi"}

{"step":"OBSERVE","tool":"get_weather","output":"The weather in Delhi is Sunny +38°C"}

{"step":"PLAN","content":"Great, I got the weather data for Delhi."}

{"step":"OUTPUT","content":"I detected that you likely meant 'Delhi' instead of 'delhiii'. The current weather in Delhi is Sunny and 38°C."}

 

Example 5: Another Misspelled City (Fuzzy Matching)

Q: What is the weather in neo yeark?

A:

{"step":"START","content":"The user wants to know the weather in neo yeark, which appears to be a misspelled city name."}

{"step":"PLAN","content":"The city name 'neo yeark' is likely a misspelling. I should check for similar city names."}

{"step":"PLAN","content":"The closest match to 'neo yeark' is 'New York'. This is a valid city name."}

{"step":"PLAN","content":"I will use the corrected city name 'New York' to fetch the weather."}

{"step":"TOOL","tool":"get_weather","input":"New York"}

{"step":"OBSERVE","tool":"get_weather","output":"The weather in New York is Cloudy +22°C"}

{"step":"PLAN","content":"Great, I got the weather data for New York."}

{"step":"OUTPUT","content":"I detected that you likely meant 'New York' instead of 'neo yeark'. The current weather in New York is Cloudy and 22°C."}

 

Example 6: Unknown City

Q: What is the weather in abc?

A:

{"step":"START","content":"The user wants to know the weather in abc."}

{"step":"PLAN","content":"The city name 'abc' appears to be invalid or a misspelling."}

{"step":"PLAN","content":"I should check for similar city names, but 'abc' does not match any known city."}

{"step":"PLAN","content":"Since no close match exists, I will attempt to fetch weather data anyway."}

{"step":"TOOL","tool":"get_weather","input":"abc"}

{"step":"OBSERVE","tool":"get_weather","output":"I don't know the weather in that city."}

{"step":"PLAN","content":"Unable to find information for 'abc'. No similar city names found."}

{"step":"OUTPUT","content":"Unable to determine the weather for 'abc'. This doesn't match any known city. Could you please verify the city name and try again?"}

 

Example 7: Network Error (requests.RequestException)

Q: What is the weather in London?

A:

{"step":"START","content":"The user wants to know the weather in London."}

{"step":"PLAN","content":"This requires real-time weather information."}

{"step":"PLAN","content":"The city name 'London' is valid. I will use the get_weather tool with this city parameter."}

{"step":"TOOL","tool":"get_weather","input":"London"}

{"step":"OBSERVE","tool":"get_weather","output":"Error fetching weather: Connection timeout exceeded"}

{"step":"PLAN","content":"The weather service is currently unavailable due to a network error."}

{"step":"OUTPUT","content":"I apologize, but I'm currently unable to fetch weather information for London due to a network connectivity issue. The weather service is temporarily unreachable. Please try again in a moment."}

"""


print("\n" * 4)


# Initialize the conversation history

message_history: list[ChatCompletionMessageParam] = [
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

    response = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        response_format={"type": "json_object"},
        messages=message_history,
    )

    content = response.choices[0].message.content

    if content is None:

        raise ValueError("The model returned no content.")

    # Save assistant response

    message_history.append(
        {
            "role": "assistant",
            "content": content,
        }
    )

    result = json.loads(content)

    parsed_result = WeatherData.model_validate(result)

    if parsed_result.step == "START":

        print(f"🔥 : {parsed_result.content}")

        # Tell the model to continue

        message_history.append(
            {
                "role": "developer",
                "content": "Proceed to the next step.",
            }
        )

    elif parsed_result.step == "PLAN":

        print(f"🧠 : {parsed_result.content}")

        # Continue reasoning

        message_history.append(
            {
                "role": "developer",
                "content": "Proceed to the next step.",
            }
        )

    elif parsed_result.step == "TOOL":

        if parsed_result.tool is None:

            raise ValueError("Tool name is missing.")

        if parsed_result.input is None:

            raise ValueError("Tool input is missing.")

        tool_name = parsed_result.tool

        tool_input = parsed_result.input

        print(f"⚒️ : {tool_name}({tool_input})")

        tool_output = available_tools[tool_name](tool_input)

        print(f"⚒️ : {tool_output}")

        # Send observation back to the model

        message_history.append(
            {
                "role": "developer",
                "content": json.dumps(
                    {
                        "step": "OBSERVE",
                        "tool": tool_name,
                        "output": tool_output,
                    }
                ),
            }
        )

    elif parsed_result.step == "OUTPUT":

        print(f"🤖 : {parsed_result.content}")

        break
