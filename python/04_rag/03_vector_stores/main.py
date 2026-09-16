# Install required packages:
#
# pip install langchain chromadb langchain-google-genai langchain-community


from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

# ============================================================
# 1. Create Gemini Embeddings
# ============================================================

embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")


# ============================================================
# 2. Create LangChain Documents
# ============================================================

doc1 = Document(
    page_content=(
        "Virat Kohli is one of the most successful and consistent batsmen "
        "in IPL history. Known for his aggressive batting style and fitness, "
        "he has led the Royal Challengers Bangalore in multiple seasons."
    ),
    metadata={"team": "Royal Challengers Bangalore"},
)

doc2 = Document(
    page_content=(
        "Rohit Sharma is the most successful captain in IPL history, "
        "leading Mumbai Indians to five titles. He's known for his calm "
        "demeanor and ability to play big innings under pressure."
    ),
    metadata={"team": "Mumbai Indians"},
)

doc3 = Document(
    page_content=(
        "MS Dhoni, famously known as Captain Cool, has led Chennai Super "
        "Kings to multiple IPL titles. His finishing skills, wicketkeeping, "
        "and leadership are legendary."
    ),
    metadata={"team": "Chennai Super Kings"},
)

doc4 = Document(
    page_content=(
        "Jasprit Bumrah is considered one of the best fast bowlers in T20 "
        "cricket. Playing for Mumbai Indians, he is known for his yorkers "
        "and death-over expertise."
    ),
    metadata={"team": "Mumbai Indians"},
)

doc5 = Document(
    page_content=(
        "Ravindra Jadeja is a dynamic all-rounder who contributes with both "
        "bat and ball. Representing Chennai Super Kings, his quick fielding "
        "and match-winning performances make him a key player."
    ),
    metadata={"team": "Chennai Super Kings"},
)

docs = [doc1, doc2, doc3, doc4, doc5]


# ============================================================
# 3. Create Chroma Vector Store
# ============================================================

vector_store = Chroma(
    collection_name="sample",
    embedding_function=embeddings,
    persist_directory="my_chroma_db",
)


# ============================================================
# 4. Add Documents
# ============================================================

ids = vector_store.add_documents(docs)

print("\nDocument IDs:")
print(ids)


# ============================================================
# 5. View Documents
# ============================================================

result = vector_store.get(include=["embeddings", "documents", "metadatas"])

print("\nAll documents:")
print(result)


# ============================================================
# 6. Similarity Search
# ============================================================

results = vector_store.similarity_search(
    query="Who among these are a bowler?",
    k=2,
)

print("\nSimilarity search:")

for document in results:
    print(document)


# ============================================================
# 7. Similarity Search With Score
# ============================================================

results_with_scores = vector_store.similarity_search_with_score(
    query="Who among these are a bowler?",
    k=2,
)

print("\nSimilarity search with scores:")

for document, score in results_with_scores:
    print(f"Score: {score}")
    print(document)


# ============================================================
# 8. Metadata Filtering
# ============================================================

# Do NOT use query="" with Gemini embeddings.
# Use a normal query together with the metadata filter.

filtered_results = vector_store.similarity_search(
    query="players",
    k=10,
    filter={"team": "Chennai Super Kings"},
)

print("\nFiltered documents:")

for document in filtered_results:
    print(document)


# ============================================================
# 9. Update Document
# ============================================================

updated_doc1 = Document(
    page_content=(
        "Virat Kohli, the former captain of Royal Challengers Bangalore "
        "(RCB), is renowned for his aggressive leadership and consistent "
        "batting performances. He holds the record for the most runs in "
        "IPL history, including multiple centuries in a single season. "
        "Despite RCB not winning an IPL title under his captaincy, Kohli's "
        "passion and fitness set a benchmark for the league. His ability "
        "to chase targets and anchor innings has made him one of the most "
        "dependable players in T20 cricket."
    ),
    metadata={"team": "Royal Challengers Bangalore"},
)

vector_store.update_documents(
    ids=[ids[0]],
    documents=[updated_doc1],
)

print("\nDocument updated.")


# ============================================================
# 10. View Documents After Update
# ============================================================

result = vector_store.get(include=["embeddings", "documents", "metadatas"])

print("\nDocuments after update:")
print(result)


# ============================================================
# 11. Delete Document
# ============================================================

vector_store.delete(ids=[ids[0]])

print("\nDocument deleted.")


# ============================================================
# 12. View Documents After Deletion
# ============================================================

result = vector_store.get(include=["embeddings", "documents", "metadatas"])

print("\nDocuments after deletion:")
print(result)
