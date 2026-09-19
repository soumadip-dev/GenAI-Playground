import os

from dotenv import load_dotenv
from langchain_classic.retrievers import ContextualCompressionRetriever
from langchain_classic.retrievers.document_compressors import LLMChainExtractor
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from rich import print

load_dotenv()


# Create the Gemini embedding model.
embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")


# Create sample documents for retrieval.
documents = [
    Document(
        page_content=(
            """The Grand Canyon is one of the most visited natural wonders in the world.
Photosynthesis is the process by which green plants convert sunlight into energy.
Millions of tourists travel to see it every year. The rocks date back millions of years."""
        ),
        metadata={"source": "Doc1"},
    ),
    Document(
        page_content=(
            """In medieval Europe, castles were built primarily for defense.
The chlorophyll in plant cells captures sunlight during photosynthesis.
Knights wore armor made of metal. Siege weapons were often used to breach castle walls."""
        ),
        metadata={"source": "Doc2"},
    ),
    Document(
        page_content=(
            """Basketball was invented by Dr. James Naismith in the late 19th century.
It was originally played with a soccer ball and peach baskets. NBA is now a global league."""
        ),
        metadata={"source": "Doc3"},
    ),
    Document(
        page_content=(
            """The history of cinema began in the late 1800s. Silent films were the earliest form.
Thomas Edison was among the pioneers. Photosynthesis does not occur in animal cells.
Modern filmmaking involves complex CGI and sound design."""
        ),
        metadata={"source": "Doc4"},
    ),
]


# Create a FAISS vector store from the documents and their embeddings.
vector_store = FAISS.from_documents(
    documents,
    embedding=embeddings,
)


# Create a base retriever from the vector store.
base_retriever = vector_store.as_retriever(search_kwargs={"k": 5})


# Get and verify the Gemini API key.
gemini_api_key = os.getenv("GOOGLE_API_KEY")

if not gemini_api_key:
    raise ValueError("GOOGLE_API_KEY environment variable is missing in the .env file.")


# Create the Gemini chat model used by the document compressor.
llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    google_api_key=gemini_api_key,
)


# Create an LLM-based document compressor.
compressor = LLMChainExtractor.from_llm(llm)


# Create a contextual compression retriever.
# The base retriever first retrieves relevant documents,
# then the compressor extracts only the parts relevant to the query.
compression_retriever = ContextualCompressionRetriever(
    base_retriever=base_retriever,
    base_compressor=compressor,
)


# User's original query.
query = "What is photosynthesis?"


# Retrieve and compress the relevant documents.
results = compression_retriever.invoke(query)


# Display the retrieved documents.
print("*" * 50)

for i, document in enumerate(results, start=1):
    print(f"Result {i}:")
    print(f"Source: {document.metadata['source']}")
    print(document.page_content)
    print()

print("*" * 50)
