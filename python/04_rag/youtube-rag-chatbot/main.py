import os
import re

from dotenv import load_dotenv

from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import (
    RunnableLambda,
    RunnableParallel,
    RunnablePassthrough,
)
from langchain_core.output_parsers import StrOutputParser

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_google_genai import (
    GoogleGenerativeAIEmbeddings,
    ChatGoogleGenerativeAI,
)

from langchain_community.vectorstores import FAISS

from langchain_classic.retrievers import ContextualCompressionRetriever
from langchain_classic.retrievers.document_compressors import LLMChainExtractor

from youtube_transcript_api import (
    YouTubeTranscriptApi,
    TranscriptsDisabled,
    NoTranscriptFound,
)

# =========================================
# CONFIG
# =========================================

LLM_MODEL_NAME = "gemini-3.5-flash-lite"
EMBEDDING_MODEL_NAME = "models/gemini-embedding-001"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
RETRIEVER_TOP_K = 5


def load_google_api_key() -> str:
    """Load environment variables and return the Gemini API key, or raise if missing."""
    load_dotenv()

    google_api_key = os.getenv("GEMINI_API_KEY")

    if not google_api_key:
        raise ValueError("GEMINI_API_KEY environment variable is missing in .env file.")

    return google_api_key


def build_llm_client(google_api_key: str) -> ChatGoogleGenerativeAI:
    """Create the Gemini chat model used for both compression and generation."""
    return ChatGoogleGenerativeAI(
        model=LLM_MODEL_NAME,
        google_api_key=google_api_key,
    )


# TODO
def build_embeddings(google_api_key: str) -> GoogleGenerativeAIEmbeddings:
    """Create the Gemini embeddings model used to index transcript chunks."""
    return GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL_NAME,
    )


# =========================================
# INDEXING
# =========================================


def extract_youtube_id(url: str) -> str | None:
    """Pull the 11-character YouTube video id out of any common URL format."""
    pattern = r"(?:v=|/embed/|/shorts/|youtu\.be/|/v/|^)([0-9A-Za-z_-]{11})"
    match = re.search(pattern, url)

    return match.group(1) if match else None


# load embeddings
def get_youtube_transcript(video_id: str, language: str | None = None) -> str:
    """Fetch and flatten the transcript for a given video id into a single string."""
    transcript_api = YouTubeTranscriptApi()

    try:
        # Get all available transcripts
        transcript_list = transcript_api.list(video_id)

        # Select the requested transcript.
        if language:
            transcript = transcript_list.find_transcript([language])
        else:
            transcript = next(iter(transcript_list))

        fetched_transcript = transcript.fetch()

        transcript_text = " ".join(snippet.text for snippet in fetched_transcript)

        return transcript_text

    except TranscriptsDisabled:
        raise ValueError("Transcripts are disabled for this video.")

    except NoTranscriptFound:
        raise ValueError(f"No transcript found for language: {language}")


# text splitting
def split_transcript_into_documents(text: str, video_id: str) -> list[Document]:
    """Chunk raw transcript text into overlapping Documents tagged with the video id."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )

    chunks = splitter.split_text(text)

    documents = [
        Document(
            page_content=chunk,
            metadata={"video_id": video_id},
        )
        for chunk in chunks
    ]

    return documents


def build_vector_store(
    documents: list[Document],
    embeddings: GoogleGenerativeAIEmbeddings,
) -> FAISS:
    """Embed and store the transcript chunks in an in-memory FAISS index."""
    return FAISS.from_documents(documents, embedding=embeddings)


def index_video(
    youtube_url: str,
    embeddings: GoogleGenerativeAIEmbeddings,
    language: str | None = None,
) -> FAISS:
    """
    End-to-end indexing pipeline for one video: URL -> id -> transcript ->
    chunks -> vector store. Each step calls the next.
    """
    video_id = extract_youtube_id(youtube_url)

    if not video_id:
        raise ValueError("Invalid YouTube URL.")

    transcript = get_youtube_transcript(video_id, language=language)
    documents = split_transcript_into_documents(transcript, video_id)
    vector_store = build_vector_store(documents, embeddings)

    return vector_store


# =========================================
# RETRIEVAL
# =========================================


def build_compression_retriever(
    vector_store: FAISS,
    llm_client: ChatGoogleGenerativeAI,
    top_k: int = RETRIEVER_TOP_K,
) -> ContextualCompressionRetriever:
    """
    Wrap a plain similarity retriever with an LLM-based compressor so only the
    passages relevant to the question are kept.
    """
    base_retriever = vector_store.as_retriever(search_kwargs={"k": top_k})
    compressor = LLMChainExtractor.from_llm(llm_client)

    return ContextualCompressionRetriever(
        base_retriever=base_retriever,
        base_compressor=compressor,
    )


def format_docs(retrieved_docs: list[Document]) -> str:
    """Format retrieved documents into a single context string."""
    return "\n\n".join(doc.page_content for doc in retrieved_docs)


# =========================================
# AUGMENTATION
# =========================================


def build_prompt_template() -> PromptTemplate:
    """
    Build the QA prompt. Improved to give the model explicit role, grounding,
    and output-formatting rules so answers stay concise, on-topic, and
    strictly evidence-based.
    """
    return PromptTemplate.from_template("""
        You are a precise research assistant answering questions about a YouTube video's transcript.

        Rules:
        - Use ONLY the information in the transcript context below. Do not use outside knowledge.
        - If the context does not contain enough information to answer, respond with exactly: I don't know
        - Always respond in English, even if the context is in another language.
        - Answer directly and concisely, in 1-3 sentences unless the question requires more detail.
        - Do not mention "the context", "the transcript", or that you were given source material.
        - Do not add disclaimers, hedging, or restate the question.

        Transcript context:
        {context}

        Question:
        {question}

        Answer:
        """)


# =========================================
# GENERATION
# =========================================


def build_qa_chain(
    retriever: ContextualCompressionRetriever,
    llm_client: ChatGoogleGenerativeAI,
):
    """Build the complete retrieval-augmented generation chain."""
    prompt = build_prompt_template()
    parser = StrOutputParser()

    parallel_chain = RunnableParallel(
        {
            "context": retriever | RunnableLambda(format_docs),
            "question": RunnablePassthrough(),
        }
    )

    main_chain = parallel_chain | prompt | llm_client | parser

    return main_chain


# =========================================
# ENTRY POINT
# =========================================


def run_pipeline(
    youtube_url: str,
    question: str,
    language: str | None = None,
) -> str:
    """
    Full pipeline for one video and one question: set up clients -> index the
    video -> build a retriever -> answer the question. Each stage calls the
    next stage's function.
    """
    google_api_key = load_google_api_key()

    llm_client = build_llm_client(google_api_key)
    embeddings = build_embeddings(google_api_key)

    vector_store = index_video(youtube_url, embeddings, language=language)
    retriever = build_compression_retriever(vector_store, llm_client)

    qa_chain = build_qa_chain(retriever, llm_client)

    return qa_chain.invoke(question)


def main() -> None:
    youtube_url = "https://youtu.be/7aEAS5E5vjg"
    question = "what is the cost of time?"

    answer = run_pipeline(youtube_url, question)

    print("*" * 50)
    print(answer)
    print("*" * 50)


if __name__ == "__main__":
    main()
