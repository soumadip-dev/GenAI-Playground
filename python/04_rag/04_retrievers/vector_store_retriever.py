from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
from rich import print

load_dotenv()


# Create Gemini embedding model
embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

# Step 1: Your source documents
documents = [
    Document(page_content="LangChain helps developers build LLM applications easily."),
    Document(
        page_content="Chroma is a vector database optimized for LLM-based search."
    ),
    Document(page_content="Embeddings convert text into high-dimensional vectors."),
    Document(page_content="OpenAI provides powerful embedding models."),
]


# Create Chroma vector store
vector_store = Chroma.from_documents(
    documents,
    collection_name="sample",
    embedding=embeddings,
    persist_directory="my_chroma_db",
)

# convert vector store to retriever
# k specifies the number of most similar documents to return
retriever = vector_store.as_retriever(search_kwargs={"k": 2})

query = "What is chroma used for?"
result = retriever.invoke(query)

for doc in result:
    print(doc.page_content)
