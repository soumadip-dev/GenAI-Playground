from langchain_community.document_loaders import (
    CSVLoader,
    DirectoryLoader,
    PyPDFLoader,
    TextLoader,
    WebBaseLoader,
)


# Loads and prints content from a single text file
def load_text_document():
    text_loader = TextLoader("data/text/poem.txt", encoding="utf-8")
    documents = text_loader.load()

    print(documents)
    print(type(documents))


# Loads and prints metadata/content from a single PDF file
def load_pdf_document():
    pdf_loader = PyPDFLoader("data/pdf/chapter1.pdf")
    documents = pdf_loader.load()

    print(f"Total pages: {len(documents)}")
    print(documents[1].page_content)
    print(documents[1].metadata)


# Loads all PDF documents in a directory into memory at once
def load_pdf_directory():
    # Requires 'pypdf' installed
    directory_loader = DirectoryLoader(
        path="data/pdf/book",
        glob="*.pdf",
        loader_cls=PyPDFLoader,  # type: ignore
    )
    documents = directory_loader.load()

    print(f"Total documents loaded: {len(documents)}")
    print(documents[5].page_content)
    print(documents[5].metadata)


# Lazy-loads PDF documents from a directory one-by-one to save memory
def lazy_load_pdf_directory():
    directory_loader = DirectoryLoader(
        path="data/pdf/book",
        glob="*.pdf",
        loader_cls=PyPDFLoader,  # type: ignore
    )
    document_stream = directory_loader.lazy_load()

    for document in document_stream:
        print(document.metadata)


# Fetches and parses content from a target website URL
def load_web_page():
    # Requires 'beautifulsoup4' installed
    target_url = "https://soumadip.vercel.app/"
    web_loader = WebBaseLoader(target_url)

    documents = web_loader.load()
    print(f"Total pages loaded: {len(documents)}")
    print(documents[0].page_content)
    print(documents[0].metadata)


# Loads and prints structured data from a CSV file (one Document per row)
def load_csv_document():
    loader = CSVLoader("data/csv/data.csv")
    documents = loader.load()

    print(documents)
    print(type(documents))
    print(documents[0].page_content)
    print(documents[0].metadata)


user_choice = int(input("Enter your choice: "))

match user_choice:
    case 1:
        load_text_document()
    case 2:
        load_pdf_document()
    case 3:
        load_pdf_directory()
    case 4:
        lazy_load_pdf_directory()
    case 5:
        load_web_page()
    case 6:
        load_csv_document()
    case _:
        print("Invalid choice")
