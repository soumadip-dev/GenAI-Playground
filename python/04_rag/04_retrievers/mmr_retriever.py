from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()


# Create the Gemini embedding model.
embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")


# Define the source documents to be embedded and stored.
documents = [
    Document(page_content="LangChain makes it easy to work with LLMs."),
    Document(page_content="LangChain is used to build LLM-based applications."),
    Document(page_content="Chroma is used to store and search document embeddings."),
    Document(page_content="Embeddings are vector representations of text."),
    Document(
        page_content="MMR helps you get diverse results when performing similarity search."
    ),
    Document(page_content="LangChain supports Chroma, FAISS, Pinecone, and more."),
]


# Create a FAISS vector store from the source documents and their embeddings.
vector_store = FAISS.from_documents(
    documents,
    embedding=embeddings,
)


# Convert the vector store into a retriever.
# "k" specifies the number of documents to retrieve.
# "lambda_mult" controls the balance between relevance and diversity.
# A value closer to 0 favors diversity, while a value closer to 1
# favors relevance.
retriever = vector_store.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 3, "lambda_mult": 0.5},
)


query = "What is LangChain?"
results = retriever.invoke(query)


# Display the retrieved documents.
print("*" * 50)

for i, document in enumerate(results):
    print(f"Result {i+1}:")
    print(document.page_content)

print("*" * 50)
