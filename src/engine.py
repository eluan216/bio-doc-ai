"""Bio-Doc AI - Engine Module
Core AI logic, RAG pipeline, and vector database integration

This module provides the RAG (Retrieval-Augmented Generation) pipeline for
semantic document analysis using LangChain, OpenAI, and FAISS.
"""

import os
import logging
from typing import Optional, List
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema import Document

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_pdf(file_path: str, max_pages: int = 5) -> str:
    """
    Load and extract text from PDF file.
    
    Args:
        file_path: Path to PDF file
        max_pages: Maximum number of pages to extract (default: 5)
        
    Returns:
        Concatenated text content from PDF pages
        
    Raises:
        FileNotFoundError: If PDF file doesn't exist
        ValueError: If PDF is empty or unreadable
    """
    if not os.path.exists(file_path):
        logger.error(f"PDF file not found: {file_path}")
        raise FileNotFoundError(f"PDF file not found: {file_path}")
    
    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()
        
        if not pages:
            logger.warning(f"No content found in PDF: {file_path}")
            raise ValueError(f"PDF appears to be empty: {file_path}")
        
        context = "\n".join([p.page_content for p in pages[:max_pages]])
        logger.info(f"Successfully loaded {len(pages)} pages from {file_path}")
        return context
        
    except Exception as e:
        logger.error(f"Error loading PDF {file_path}: {str(e)}")
        raise


def create_vector_store(file_path: str, api_key: str) -> FAISS:
    """
    Create FAISS vector store from PDF document.
    Enables semantic search and RAG capabilities.
    
    Args:
        file_path: Path to PDF file
        api_key: OpenAI API key for embeddings
        
    Returns:
        FAISS vector store object
        
    Raises:
        ValueError: If document loading or embedding fails
    """
    if not api_key:
        raise ValueError("OpenAI API key is required")
    
    try:
        os.environ["OPENAI_API_KEY"] = api_key
        
        # Load PDF
        loader = PyPDFLoader(file_path)
        documents: List[Document] = loader.load()
        
        if not documents:
            raise ValueError(f"No documents loaded from {file_path}")
        
        # Split into chunks for better retrieval
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        chunks = text_splitter.split_documents(documents)
        logger.info(f"Created {len(chunks)} text chunks from document")
        
        # Create embeddings and vector store
        embeddings = OpenAIEmbeddings(api_key=api_key)
        vector_store = FAISS.from_documents(chunks, embeddings)
        logger.info("Vector store created successfully")
        
        return vector_store
        
    except Exception as e:
        logger.error(f"Error creating vector store: {str(e)}")
        raise ValueError(f"Failed to create vector store: {str(e)}")


def retrieve_context(vector_store: FAISS, query: str, k: int = 5) -> str:
    """
    Retrieve relevant context from vector store using semantic search.
    
    Args:
        vector_store: FAISS vector store object
        query: User query/question for similarity search
        k: Number of relevant chunks to retrieve (default: 5)
        
    Returns:
        Concatenated relevant context
        
    Raises:
        ValueError: If retrieval fails
    """
    try:
        if not query or not query.strip():
            raise ValueError("Query cannot be empty")
        
        results = vector_store.similarity_search(query, k=k)
        
        if not results:
            logger.warning(f"No similar documents found for query: {query}")
            return ""
        
        context = "\n".join([doc.page_content for doc in results])
        logger.info(f"Retrieved {len(results)} similar documents")
        return context
        
    except Exception as e:
        logger.error(f"Error retrieving context: {str(e)}")
        raise ValueError(f"Failed to retrieve context: {str(e)}")


def initialize_llm(api_key: str) -> ChatOpenAI:
    """
    Initialize OpenAI LLM with API key.
    
    Args:
        api_key: OpenAI API key
        
    Returns:
        Initialized ChatOpenAI instance
        
    Raises:
        ValueError: If API key is invalid
    """
    if not api_key:
        raise ValueError("OpenAI API key is required")
    
    try:
        os.environ["OPENAI_API_KEY"] = api_key
        llm = ChatOpenAI(model="gpt-4o-mini")
        logger.info("LLM initialized successfully")
        return llm
    except Exception as e:
        logger.error(f"Error initializing LLM: {str(e)}")
        raise ValueError(f"Failed to initialize LLM: {str(e)}")


def query_document(llm: ChatOpenAI, context: str, question: str) -> str:
    """
    Query document context with LLM.
    
    Args:
        llm: ChatOpenAI instance
        context: Document context for the query
        question: User question
        
    Returns:
        AI-generated response
        
    Raises:
        ValueError: If query fails
    """
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
        logger.error(f"Error querying document: {str(e)}")
        raise ValueError(f"Failed to query document: {str(e)}")


def get_ai_response(
    file_path: str,
    user_query: str,
    api_key: str,
    use_vector_search: bool = True
) -> str:
    """
    End-to-end function: Load PDF and get AI response with optional vector search.
    
    This is the main entry point for document querying. It handles the complete
    pipeline from document loading to AI response generation.
    
    Args:
        file_path: Path to PDF file
        user_query: User's question about the document
        api_key: OpenAI API key
        use_vector_search: Enable FAISS vector search for better retrieval (default: True)
        
    Returns:
        AI-generated response based on document context
        
    Raises:
        FileNotFoundError: If PDF file doesn't exist
        ValueError: If any step in the pipeline fails
    """
    logger.info(f"Processing query: {user_query[:50]}...")
    
    try:
        # Initialize LLM
        llm = initialize_llm(api_key)
        
        # Retrieve context - use vector search if enabled
        if use_vector_search:
            logger.info("Using vector search for context retrieval")
            vector_store = create_vector_store(file_path, api_key)
            context = retrieve_context(vector_store, user_query)
        else:
            logger.info("Using simple document loading")
            context = load_pdf(file_path)
        
        # Query document with LLM
        response = query_document(llm, context, user_query)
        logger.info("Response generated successfully")
        
        return response
        
    except Exception as e:
        logger.error(f"Error in get_ai_response: {str(e)}")
        raise
