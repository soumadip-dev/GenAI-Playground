from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter

loader = PyPDFLoader("data/pdf/chapter1.pdf")
docs = loader.load()

splitter = CharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=0,
    separator="",
)

result = splitter.split_documents(docs)

print("*" * 50)
print(result[1].page_content)
print("*" * 50)
