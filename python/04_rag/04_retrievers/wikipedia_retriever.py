from langchain_community.retrievers import WikipediaRetriever
from rich import print

# Create the Wikipedia retriever.
# "top_k_results" specifies the maximum number of results to retrieve.
# "doc_content_chars_max" limits the amount of content returned for each document.
retriever = WikipediaRetriever(
    top_k_results=3,
    doc_content_chars_max=2000,
)


# Define the search query.
query = "What is LangChain?"


# Retrieve relevant documents from Wikipedia.
results = retriever.invoke(query)


# Display the retrieved documents.
for document in results:
    print(document.page_content)
