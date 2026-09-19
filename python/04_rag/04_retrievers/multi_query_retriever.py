import os

from dotenv import load_dotenv
from langchain_classic.retrievers import MultiQueryRetriever
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from rich import print

load_dotenv()


# Create the Gemini embedding model.
embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")


# Relevant health and wellness documents.
documents = [
    Document(
        page_content="Regular walking boosts heart health and can reduce symptoms of depression.",
        metadata={"source": "H1"},
    ),
    Document(
        page_content="Consuming leafy greens and fruits helps detox the body and improve longevity.",
        metadata={"source": "H2"},
    ),
    Document(
        page_content="Deep sleep is crucial for cellular repair and emotional regulation.",
        metadata={"source": "H3"},
    ),
    Document(
        page_content="Mindfulness and controlled breathing lower cortisol and improve mental clarity.",
        metadata={"source": "H4"},
    ),
    Document(
        page_content="Drinking sufficient water throughout the day helps maintain metabolism and energy.",
        metadata={"source": "H5"},
    ),
    Document(
        page_content="The solar energy system in modern homes helps balance electricity demand.",
        metadata={"source": "I1"},
    ),
    Document(
        page_content="Python balances readability with power, making it a popular system design language.",
        metadata={"source": "I2"},
    ),
    Document(
        page_content="Photosynthesis enables plants to produce energy by converting sunlight.",
        metadata={"source": "I3"},
    ),
    Document(
        page_content="The 2022 FIFA World Cup was held in Qatar and drew global energy and excitement.",
        metadata={"source": "I4"},
    ),
    Document(
        page_content="Black holes bend spacetime and store immense gravitational energy.",
        metadata={"source": "I5"},
    ),
]


# Create a FAISS vector store from the documents and their embeddings.
vector_store = FAISS.from_documents(
    documents,
    embedding=embeddings,
)


# Gemini model used by the MultiQueryRetriever to generate alternative queries.
gemini_model_name = "gemini-3.5-flash-lite"


# Get and verify the Gemini API key.
gemini_api_key = os.getenv("GOOGLE_API_KEY")

if not gemini_api_key:
    raise ValueError("GOOGLE_API_KEY environment variable is missing in the .env file.")


# Create a MultiQueryRetriever that generates multiple versions
# of the user's query to improve document retrieval.
retriever = MultiQueryRetriever.from_llm(
    retriever=vector_store.as_retriever(search_kwargs={"k": 5}),
    llm=ChatGoogleGenerativeAI(
        model=gemini_model_name,
        google_api_key=gemini_api_key,
    ),
)


# User's original query.
query = "How to improve energy levels and maintain balance?"


# Retrieve relevant documents using multiple generated queries.
results = retriever.invoke(query)


# Display the retrieved documents.
print("*" * 50)

for i, document in enumerate(results, start=1):
    print(f"Result {i}:")
    print(f"Source: {document.metadata['source']}")
    print(document.page_content)
    print()

print("*" * 50)
