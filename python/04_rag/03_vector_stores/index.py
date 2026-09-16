from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
from rich import print

load_dotenv()


# Create Gemini embedding model
embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")


# Create LangChain documents
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

documents = [doc1, doc2, doc3, doc4, doc5]


# Create Chroma vector store
vector_store = Chroma(
    collection_name="sample",
    embedding_function=embeddings,
    persist_directory="my_chroma_db",
)


# Add documents to the vector store
document_ids = vector_store.add_documents(documents)

print("\n[bold red]Document IDs:[/bold red]")
print(document_ids)


# Retrieve and display stored documents, metadata, and embeddings
documents_data = vector_store.get(include=["embeddings", "documents", "metadatas"])

print("\n[bold cyan]Documents:[/bold cyan]")
for document in documents_data["documents"]:
    print(document, "\n")


print("\n[bold cyan]Metadata:[/bold cyan]")
for metadata in documents_data["metadatas"]:
    print(metadata, "\n")


print("\n[bold cyan]Embeddings:[/bold cyan]")
for embedding in documents_data["embeddings"]:
    print(embedding, "\n")


# Perform a similarity search
# k specifies the number of most similar documents to return
similar_documents = vector_store.similarity_search(
    query="Who among these are a bowler?",
    k=2,
)

print("\n[bold blue]Similarity Search Results:[/bold blue]")
for document in similar_documents:
    print(f"[green]{document}[/green]")


# Perform a similarity search and return similarity scores
similar_documents_with_scores = vector_store.similarity_search_with_score(
    query="Who among these are a bowler?",
    k=2,
)

print("\n[bold blue]Similarity Search Results with Scores:[/bold blue]")
for document, score in similar_documents_with_scores:
    print(f"[yellow]Score: {score}[/yellow]")
    print(document)


# Perform a similarity search with metadata filtering
filtered_documents = vector_store.similarity_search(
    query="players",
    k=10,
    filter={"team": "Chennai Super Kings"},
)

print("\n[bold blue]Filtered Documents:[/bold blue]")
for document in filtered_documents:
    print(document)


# Update an existing document
updated_doc1 = Document(
    page_content=(
        "Virat Kohli, the former captain of Royal Challengers Bangalore (RCB), "
        "is renowned for his aggressive leadership and consistent batting "
        "performances. He holds the record for the most runs in IPL history, "
        "including multiple centuries in a single season. Despite RCB not "
        "winning an IPL title under his captaincy, Kohli's passion and fitness "
        "set a benchmark for the league. His ability to chase targets and "
        "anchor innings has made him one of the most dependable players in "
        "T20 cricket."
    ),
    metadata={"team": "Royal Challengers Bangalore"},
)

vector_store.update_document(
    document_id=document_ids[0],
    document=updated_doc1,
)


# Retrieve the documents after the update
updated_documents_data = vector_store.get(include=["documents", "metadatas"])

print("\n[bold cyan]Documents After Update:[/bold cyan]")
for document in updated_documents_data["documents"]:
    print(document, "\n")


# Delete the first document from the vector store
vector_store.delete(ids=[document_ids[0]])


# Retrieve the documents after deletion
remaining_documents_data = vector_store.get(include=["documents", "metadatas"])

print("\n[bold cyan]Documents After Deletion:[/bold cyan]")
for document in remaining_documents_data["documents"]:
    print(document, "\n")
