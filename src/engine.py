"""Bio-Doc AI - Engine Module
Core AI logic, RAG pipeline, and vector database integration.

RAG pipeline for biomedical document analysis using LangChain, OpenAI, and FAISS.
"""

from __future__ import annotations

import logging
import os
from typing import TYPE_CHECKING, Any, List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

_DEPS_ERROR = (
    "Missing Bio-Doc AI dependencies. Install with:\n"
    "  pip install -r requirements.txt\n"
    "Required packages include: langchain-openai, langchain-community, "
    "langchain-text-splitters, faiss-cpu, pypdf, openai."
)


def _require_langchain() -> None:
    """Import LangChain stack on first use; raise a clear error if missing."""
    try:
        import langchain_openai  # noqa: F401
        import langchain_community  # noqa: F401
        import langchain_text_splitters  # noqa: F401
        import langchain_core  # noqa: F401
    except ImportError as e:
        raise ImportError(f"{_DEPS_ERROR}\nUnderlying error: {e}") from e


if TYPE_CHECKING:
    from langchain_community.vectorstores import FAISS
    from langchain_openai import ChatOpenAI


def load_pdf(file_path: str, max_pages: int = 5) -> str:
    """
    Load and extract text from a PDF file.

    Args:
        file_path: Path to PDF file.
        max_pages: Maximum number of pages to extract (default: 5).

    Returns:
        Concatenated text content from PDF pages.
    """
    _require_langchain()
    from langchain_community.document_loaders import PyPDFLoader

    if not os.path.exists(file_path):
        logger.error("PDF file not found: %s", file_path)
        raise FileNotFoundError(f"PDF file not found: {file_path}")

    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()

        if not pages:
            logger.warning("No content found in PDF: %s", file_path)
            raise ValueError(f"PDF appears to be empty: {file_path}")

        context = "\n".join([p.page_content for p in pages[:max_pages]])
        logger.info("Successfully loaded %s pages from %s", len(pages), file_path)
        return context

    except (FileNotFoundError, ValueError):
        raise
    except Exception as e:
        logger.error("Error loading PDF %s: %s", file_path, e)
        raise


def create_vector_store(file_path: str, api_key: str) -> Any:
    """
    Create a FAISS vector store from a PDF document.

    Args:
        file_path: Path to PDF file.
        api_key: OpenAI API key for embeddings.

    Returns:
        FAISS vector store object.
    """
    _require_langchain()
    from langchain_community.document_loaders import PyPDFLoader
    from langchain_community.vectorstores import FAISS
    from langchain_openai import OpenAIEmbeddings
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_core.documents import Document

    if not api_key:
        raise ValueError("OpenAI API key is required")

    try:
        os.environ["OPENAI_API_KEY"] = api_key

        loader = PyPDFLoader(file_path)
        documents: List[Document] = loader.load()

        if not documents:
            raise ValueError(f"No documents loaded from {file_path}")

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.split_documents(documents)
        logger.info("Created %s text chunks from document", len(chunks))

        embeddings = OpenAIEmbeddings(api_key=api_key)
        vector_store = FAISS.from_documents(chunks, embeddings)
        logger.info("Vector store created successfully")

        return vector_store

    except ValueError:
        raise
    except Exception as e:
        logger.error("Error creating vector store: %s", e)
        raise ValueError(f"Failed to create vector store: {e}") from e


def retrieve_context(vector_store: Any, query: str, k: int = 5) -> str:
    """Retrieve relevant context from a FAISS vector store."""
    try:
        if not query or not query.strip():
            raise ValueError("Query cannot be empty")

        results = vector_store.similarity_search(query, k=k)

        if not results:
            logger.warning("No similar documents found for query: %s", query)
            return ""

        context = "\n".join([doc.page_content for doc in results])
        logger.info("Retrieved %s similar documents", len(results))
        return context

    except ValueError:
        raise
    except Exception as e:
        logger.error("Error retrieving context: %s", e)
        raise ValueError(f"Failed to retrieve context: {e}") from e


def initialize_llm(api_key: str) -> Any:
    """Initialize OpenAI chat model with the given API key."""
    _require_langchain()
    from langchain_openai import ChatOpenAI

    if not api_key:
        raise ValueError("OpenAI API key is required")

    try:
        os.environ["OPENAI_API_KEY"] = api_key
        llm = ChatOpenAI(model="gpt-4o-mini")
        logger.info("LLM initialized successfully")
        return llm
    except Exception as e:
        logger.error("Error initializing LLM: %s", e)
        raise ValueError(f"Failed to initialize LLM: {e}") from e


def query_document(llm: Any, context: str, question: str) -> str:
    """Query document context with the LLM."""
    if not context or not context.strip():
        logger.warning("Empty context provided for query")

    if not question or not question.strip():
        raise ValueError("Question cannot be empty")

    try:
        prompt = f"Context: {context}\n\nQuestion: {question}"
        response = llm.invoke(prompt)
        logger.info("Query processed successfully")
        return response.content
    except Exception as e:
        logger.error("Error querying document: %s", e)
        raise ValueError(f"Failed to query document: {e}") from e


def get_ai_response(
    file_path: str,
    user_query: str,
    api_key: str,
    use_vector_search: bool = True,
) -> str:
    """
    End-to-end: load PDF and return an AI response with optional vector search.

    Requires OPENAI_API_KEY (or api_key argument) and packages from requirements.txt.
    """
    logger.info("Processing query: %s...", user_query[:50])

    try:
        llm = initialize_llm(api_key)

        if use_vector_search:
            logger.info("Using vector search for context retrieval")
            vector_store = create_vector_store(file_path, api_key)
            context = retrieve_context(vector_store, user_query)
        else:
            logger.info("Using simple document loading")
            context = load_pdf(file_path)

        response = query_document(llm, context, user_query)
        logger.info("Response generated successfully")
        return response

    except Exception as e:
        logger.error("Error in get_ai_response: %s", e)
        raise
