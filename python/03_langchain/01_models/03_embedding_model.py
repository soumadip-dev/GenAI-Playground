import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Load environment variables from .env file
load_dotenv()

# Verify API key existence
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable is missing in .env file.")

# Initialize the Google Generative AI Embeddings model
embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001",
    output_dimensionality=128,
)

# 1. Single Query Embedding
query_text = "Delhi is the capital of India"
query_response = embeddings.embed_query(query_text)

# 2. Batch Documents Embedding
documents = [
    "Delhi is the capital of India",
    "The capital of France is Paris.",
    "The capital of Germany is Berlin.",
]
doc_embeddings = embeddings.embed_documents(documents)

# --- SINGLE QUERY OUTPUT ---
print("=" * 70)
print("QUERY EMBEDDING VECTOR: \n")
print(query_response)
print("=" * 70)

print("\n" + "#" * 80 + "\n")  # Visual separator between query and documents

# --- DOCUMENTS OUTPUT ---
print("=" * 70)
print("DOCUMENTS EMBEDDING VECTORS: \n")
print(doc_embeddings)
print("=" * 70)
