import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
model_name = os.getenv("MODEL_NAME", "gemini-1.5-pro")

if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable is missing in .env file.")

chat_model = ChatGoogleGenerativeAI(
    model=model_name,
    temperature=0.5,
    google_api_key=api_key,
)

system_instruction = (
    "You are a senior software engineer with 15+ years of experience.\n"
    "Your responsibilities:\n"
    "- Write clean, optimized, production-ready code\n"
    "- Explain your solution in simple language\n"
    "- Mention time and space complexity where applicable\n"
    "- Suggest industry best practices and standard design patterns."
)

prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", system_instruction),
        ("human", "{user_query}"),
    ]
)


def main() -> None:
    print("AI Coding Assistant Initialized. Type 'exit' to quit.\n" + "=" * 50)

    while True:
        try:
            user_input = input("\nEnter your question: ").strip()
            if not user_input:
                continue

            if user_input.lower() in {"exit", "quit"}:
                print("\nThank you for using AI Coding Assistant. Goodbye!")
                break

            print("\nGenerating response...\n")

            # Step 1: Format the prompt template into a PromptValue object using user input
            formatted_prompt = prompt_template.invoke({"user_query": user_input})

            # Step 2: Pass the formatted prompt directly to the LLM model
            ai_response = chat_model.invoke(formatted_prompt)

            print("=" * 70)
            print(ai_response.content[0]["text"])  # type: ignore
            print("\n" + "=" * 70)

        except KeyboardInterrupt:
            print("\n\nSession terminated by user.")
            break
        except Exception as error:
            print(f"\nAn error occurred while generating the response: {error}")


if __name__ == "__main__":
    main()
