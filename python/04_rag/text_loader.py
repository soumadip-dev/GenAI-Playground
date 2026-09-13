# from langchain_community.document_loaders import TextLoader

# loader = TextLoader("cricket.txt", encoding="utf-8")

# docs = loader.load()

# print(type(docs))


from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("dl-curriculum.pdf")

docs = loader.load()

print(len(docs))
print(docs[0].page_content)
print(docs[0].metadata)
