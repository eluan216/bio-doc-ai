"""Bio-Doc AI - Engine Module
Core AI logic, RAG pipeline, and vector database integration
"""

import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter


def load_pdf(file_path: str, max_pages: int = 5) -> str:
    """Load and extract text from PDF file"""
    loader = PyPDFLoader(file_path)
    pages = loader.load_and_split()
    context = "\n".join([p.page_content for p in pages[:max_pages]])
    return context


def create_vector_store(file_path: str, api_key: str) -> FAISS:
    """
    Create FAISS vector store from PDF document
    Enables semantic search and RAG capabilities
    
    Args:
        file_path: Path to PDF file
        api_key: OpenAI API key for embeddings
        
    Returns:
        FAISS vector store object
    """
    os.environ["OPENAI_API_KEY"] = api_key
    
    # Load PDF
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    
    # Split into chunks for better retrieval
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = text_splitter.split_documents(documents)
    
    # Create embeddings and vector store
    embeddings = OpenAIEmbeddings(api_key=api_key)
    vector_store = FAISS.from_documents(chunks, embeddings)
    
    return vector_store


def retrieve_context(vector_store: FAISS, query: str, k: int = 5) -> str:
    """
    Retrieve relevant context from vector store using semantic search
    
    Args:
        vector_store: FAISS vector store
        query: User query/question
        k: Number of relevant chunks to retrieve
        
    Returns:
        Concatenated relevant context
    """
    results = vector_store.similarity_search(query, k=k)
    context = "\n".join([doc.page_content for doc in results])
    return context


def initialize_llm(api_key: str) -> ChatOpenAI:
    """Initialize OpenAI LLM with API key"""
    os.environ["OPENAI_API_KEY"] = api_key
    return ChatOpenAI(model="gpt-4o-mini")


def query_document(llm: ChatOpenAI, context: str, question: str) -> str:
    """Query document context with LLM"""
    response = llm.invoke(f"Context: {context}\n\nQuestion: {question}")
    return response.content


def get_ai_response(file_path: str, user_query: str, api_key: str, use_vector_search: bool = True) -> str:
    """
    End-to-end function: Load PDF and get AI response with optional vector search
    
    Args:
        file_path: Path to PDF file
        user_query: User's question
        api_key: OpenAI API key
        use_vector_search: Enable FAISS vector search for better retrieval
        
    Returns:
        AI-generated response based on document context
    """
    # Initialize LLM
    llm = initialize_llm(api_key)
    
    # Retrieve context - use vector search if enabled, else fallback to simple loading
    if use_vector_search:
        vector_store = create_vector_store(file_path, api_key)
        context = retrieve_context(vector_store, user_query)
    else:
        context = load_pdf(file_path)
    
    # Query document with LLM
    response = query_document(llm, context, user_query)
    
    return response
