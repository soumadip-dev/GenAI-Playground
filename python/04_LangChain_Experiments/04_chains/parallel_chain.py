# -----------------------------------------------------------------------------
# Parallel Chain
#
# Workflow:
# 1. Accept a large document as input.
# 2. Generate study notes using the Groq model.
# 3. Generate a quiz using the Gemini model.
# 4. Execute both tasks in parallel.
# 5. Merge the notes and quiz into a single study guide using Gemini.
# -----------------------------------------------------------------------------

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from rich import print

# Load environment variables from the .env file
load_dotenv()


# Model used for generating study notes
groq_chat_model = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.5,
)

# Model used for generating quizzes and combining the final output
gemini_chat_model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    temperature=0.5,
)

# -----------------------------------------------------------------------------
# Prompt Templates
# -----------------------------------------------------------------------------

# Prompt for generating study notes
study_notes_prompt = PromptTemplate.from_template("""
You are an expert note-taking assistant.

Read the following text and create well-structured study notes.
Highlight the key concepts, important points, and definitions.
Format the notes using clear headings and bullet points.

Text:
{text}
""")

# Prompt for generating quiz questions
quiz_generation_prompt = PromptTemplate.from_template("""
You are an expert quiz generator.

Read the following text and create a study quiz.
Include a variety of question types such as:
- Multiple Choice
- True/False

Text:
{text}
""")

# Prompt for combining notes and quiz
study_guide_prompt = PromptTemplate.from_template("""
You are an educational content organizer.

Combine the following study notes and quiz into a single,
well-formatted study guide.

Study Notes:
{notes}

Quiz:
{quiz}

Return the result in plain text format no md or html.
""")


# Output Parser : Converts the model responses into plain Python strings.
string_output_parser = StrOutputParser()

# -----------------------------------------------------------------------------
# Parallel Chain
#
# Both tasks execute simultaneously:
#
#                Input Document
#                     │
#         ┌───────────┴───────────┐
#         │                       │
#   Generate Notes         Generate Quiz
#      (Groq)                (Gemini)
#         │                       │
#         └───────────┬───────────┘
#                     │
#              {"notes", "quiz"}
# -----------------------------------------------------------------------------
parallel_generation_chain = RunnableParallel(
    notes=study_notes_prompt | groq_chat_model | string_output_parser,
    quiz=quiz_generation_prompt | gemini_chat_model | string_output_parser,
)

# Merge Chain : Combines the generated notes and quiz into a single study guide.
study_guide_chain = study_guide_prompt | gemini_chat_model | string_output_parser

# -----------------------------------------------------------------------------
# Final Chain
#
# Document
#    ↓
# Parallel Generation
#    ↓
# Study Guide Generation
# -----------------------------------------------------------------------------
final_chain = parallel_generation_chain | study_guide_chain

# -----------------------------------------------------------------------------
# Sample document
# -----------------------------------------------------------------------------
document_text = """
Node.js is an open-source, cross-platform JavaScript runtime environment that allows developers to execute JavaScript code outside of a web browser. It is built on Google's V8 JavaScript engine, which compiles JavaScript directly into machine code, making it fast and efficient. Before Node.js, JavaScript was primarily used for client-side scripting in web browsers. Node.js expanded the language's capabilities by enabling server-side development, allowing developers to build complete web applications using JavaScript for both the frontend and backend.

One of the most important features of Node.js is its event-driven, non-blocking I/O architecture. Traditional web servers often process requests synchronously, meaning one request may need to finish before another can be handled. Node.js, however, uses asynchronous programming to handle multiple operations simultaneously without blocking the execution of other tasks. This design makes Node.js highly efficient for applications that involve many concurrent connections, such as chat applications, streaming platforms, online gaming servers, and real-time collaboration tools.

Node.js operates on a single-threaded event loop. Although it uses only one main thread to execute JavaScript code, it can efficiently manage thousands of concurrent client requests by delegating expensive operations such as file system access, network communication, or database queries to the operating system or a thread pool. Once these operations complete, callbacks, promises, or async/await mechanisms are used to continue processing the results. This event loop is one of the primary reasons why Node.js performs exceptionally well for I/O-intensive applications.
"""

# -----------------------------------------------------------------------------
# Execute the chain
# -----------------------------------------------------------------------------
result = final_chain.invoke(
    {
        "text": document_text,
    }
)


print(result)

# Visualize the chain structure
final_chain.get_graph().print_ascii()
