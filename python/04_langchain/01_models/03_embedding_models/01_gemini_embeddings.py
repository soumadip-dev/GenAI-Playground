from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    output_dimensionality=128,
)

response = embeddings.embed_query("Delhi is the capital of India")

print(response)
print(len(response))
