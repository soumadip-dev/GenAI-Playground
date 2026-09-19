import os
import re

from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import (
    RunnableLambda,
    RunnableParallel,
    RunnablePassthrough,
)
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


# =========================================
# GOOGLE AI
# =========================================


def load_google_api_key() -> str:
    """Load the Gemini API key from the environment."""
    load_dotenv()

    google_api_key = os.getenv("GEMINI_API_KEY")

    if not google_api_key:
        raise ValueError("GEMINI_API_KEY environment variable is missing in .env file.")

    return google_api_key


def build_llm_client(google_api_key: str) -> ChatGoogleGenerativeAI:
    """Create the Gemini chat model."""
    return ChatGoogleGenerativeAI(
        model=LLM_MODEL_NAME,
        google_api_key=google_api_key,
    )


def build_embeddings(
    google_api_key: str,
) -> GoogleGenerativeAIEmbeddings:
    """Create the Gemini embedding model."""
    return GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL_NAME,
    )


# =========================================
# INDEXING
# =========================================


def extract_youtube_id(url: str) -> str | None:
    """Extract the YouTube video ID from a YouTube URL."""

    pattern = r"(?:v=|/embed/|/shorts/|youtu\.be/|/v/|^)" r"([0-9A-Za-z_-]{11})"

    match = re.search(pattern, url)

    return match.group(1) if match else None


def get_youtube_transcript(
    video_id: str,
    language: str | None = None,
) -> str:
    """Fetch and combine the transcript into a single string."""

    transcript_api = YouTubeTranscriptApi()

    try:
        transcript_list = transcript_api.list(video_id)

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


def split_transcript_into_documents(
    text: str,
    video_id: str,
) -> list[Document]:
    """Split transcript text into overlapping document chunks."""

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )

    chunks = splitter.split_text(text)

    return [
        Document(
            page_content=chunk,
            metadata={"video_id": video_id},
        )
        for chunk in chunks
    ]


def build_vector_store(
    documents: list[Document],
    embeddings: GoogleGenerativeAIEmbeddings,
) -> FAISS:
    """Create an in-memory FAISS vector store."""

    return FAISS.from_documents(
        documents,
        embedding=embeddings,
    )


def index_video(
    youtube_url: str,
    embeddings: GoogleGenerativeAIEmbeddings,
    language: str | None = None,
) -> FAISS:
    """Create a FAISS index from a YouTube video's transcript."""

    video_id = extract_youtube_id(youtube_url)

    if not video_id:
        raise ValueError("Invalid YouTube URL.")

    transcript = get_youtube_transcript(
        video_id,
        language=language,
    )

    documents = split_transcript_into_documents(
        transcript,
        video_id,
    )

    return build_vector_store(
        documents,
        embeddings,
    )


# =========================================
# RETRIEVAL
# =========================================


def build_compression_retriever(
    vector_store: FAISS,
    llm_client: ChatGoogleGenerativeAI,
    top_k: int = RETRIEVER_TOP_K,
) -> ContextualCompressionRetriever:
    """Create a contextual compression retriever."""

    base_retriever = vector_store.as_retriever(search_kwargs={"k": top_k})

    compressor = LLMChainExtractor.from_llm(llm_client)

    return ContextualCompressionRetriever(
        base_retriever=base_retriever,
        base_compressor=compressor,
    )


def format_docs(
    retrieved_docs: list[Document],
) -> str:
    """Combine retrieved documents into one context string."""

    return "\n\n".join(document.page_content for document in retrieved_docs)


# =========================================
# AUGMENTATION
# =========================================


def build_prompt_template() -> PromptTemplate:
    """Create the prompt used for question answering."""

    return PromptTemplate.from_template("""
You are a precise research assistant answering questions
about a YouTube video's transcript.

Rules:
- Use ONLY the information in the transcript context below.
- Do not use outside knowledge.
- If the context does not contain enough information to answer,
  respond with exactly: I don't know
- Always respond in English.
- Answer directly and concisely, in 1-3 sentences unless
  the question requires more detail.
- Do not mention "the context", "the transcript", or
  that you were given source material.
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
    """Build the complete RAG question-answering chain."""

    prompt = build_prompt_template()
    parser = StrOutputParser()

    parallel_chain = RunnableParallel(
        {
            "context": retriever | RunnableLambda(format_docs),
            "question": RunnablePassthrough(),
        }
    )

    return parallel_chain | prompt | llm_client | parser


# =========================================
# PIPELINE
# =========================================


def run_pipeline(
    youtube_url: str,
    question: str,
    language: str | None = None,
) -> str:
    """
    Run the complete YouTube RAG pipeline.

    URL
      ↓
    YouTube Transcript
      ↓
    Text Splitting
      ↓
    FAISS
      ↓
    Similarity Retrieval
      ↓
    Contextual Compression
      ↓
    Gemini
      ↓
    Answer
    """

    google_api_key = load_google_api_key()

    llm_client = build_llm_client(google_api_key)

    embeddings = build_embeddings(google_api_key)

    vector_store = index_video(
        youtube_url,
        embeddings,
        language=language,
    )

    retriever = build_compression_retriever(
        vector_store,
        llm_client,
    )

    qa_chain = build_qa_chain(
        retriever,
        llm_client,
    )

    return qa_chain.invoke(question)


# =========================================
# CLI ENTRY POINT
# =========================================


def main() -> None:
    youtube_url = input("Enter YouTube URL: ").strip()
    question = input("Enter your question: ").strip()

    answer = run_pipeline(
        youtube_url,
        question,
    )

    print("\n" + "=" * 50)
    print(answer)
    print("=" * 50)


if __name__ == "__main__":
    main()
