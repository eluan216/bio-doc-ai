import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader
import os

st.title("🩺 Bio-Doc AI Assistant")
st.write("Upload a Medical PDF to analyze it with AI.")

# Get API Key from environment
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("OpenAI API Key not configured. Please add it to Streamlit secrets.")
    st.stop()

uploaded_file = st.file_input("Choose a Medical PDF", type="pdf")

if uploaded_file and api_key:
    # Save file temporarily
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Load and Read PDF
    loader = PyPDFLoader("temp.pdf")
    pages = loader.load_and_split()
    context = "\n".join([p.page_content for p in pages[:3]]) # First 3 pages for speed

    # Chat Input
    user_query = st.text_input("Ask a question about this document:")
    
    if user_query:
        os.environ["OPENAI_API_KEY"] = api_key
        llm = ChatOpenAI(model="gpt-4o-mini")
        response = llm.invoke(f"Context: {context}\n\nQuestion: {user_query}")
        st.write("### AI Response:")
        st.info(response.content)