"""Bio-Doc AI - Engine Module
Core AI logic and LangChain integration
"""

import os
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader


def load_pdf(file_path: str, max_pages: int = 5) -> str:
    """Load and extract text from PDF file"""
    loader = PyPDFLoader(file_path)
    pages = loader.load_and_split()
    context = "\n".join([p.page_content for p in pages[:max_pages]])
    return context


def initialize_llm(api_key: str) -> ChatOpenAI:
    """Initialize OpenAI LLM with API key"""
    os.environ["OPENAI_API_KEY"] = api_key
    return ChatOpenAI(model="gpt-4o-mini")


def query_document(llm: ChatOpenAI, context: str, question: str) -> str:
    """Query document context with LLM"""
    response = llm.invoke(f"Context: {context}\n\nQuestion: {question}")
    return response.content
