import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="Bio-Doc AI Pro", page_icon="🩺", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007BFF; color: white; }
    .stTextInput>div>div>input { border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: Settings ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3063/3063176.png", width=100)
    st.title("Settings")
    # Try to get API key from environment first (for Streamlit Cloud), fall back to user input
    api_key = os.getenv("OPENAI_API_KEY") or st.text_input("Enter OpenAI API Key", type="password", help="Get your key at platform.openai.com")
    st.info("B.Sc. Biomedical Tech (UNIPORT) Portfolio Project")

# --- MAIN UI ---
st.title("🩺 Bio-Doc AI Assistant")
st.caption("Professional Medical Document Intelligence Platform")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Layout: Two columns for File Upload and Chat
col1, col2 = st.columns([1, 2], gap="large")

with col1:
    st.subheader("📁 Upload Document")
    uploaded_file = st.file_uploader("Upload a Medical PDF", type="pdf", label_visibility="collapsed")
    
    if uploaded_file and api_key:
        with st.spinner("Analyzing document..."):
            with open("temp.pdf", "wb") as f:
                f.write(uploaded_file.getbuffer())
            loader = PyPDFLoader("temp.pdf")
            pages = loader.load_and_split()
            context = "\n".join([p.page_content for p in pages[:5]])
            st.success("Analysis Complete!")
            st.button("📄 Generate Executive Summary", type="secondary")

with col2:
    st.subheader("💬 Clinical Consultation")
    # Display Chat History
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask about the clinical data..."):
        if not api_key:
            st.error("Please enter your API Key in the sidebar.")
        else:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                try:
                    os.environ["OPENAI_API_KEY"] = api_key
                    llm = ChatOpenAI(model="gpt-4o-mini")
                    response = llm.invoke(f"Context: {context}\n\nQuestion: {prompt}")
                    st.markdown(response.content)
                    st.session_state.messages.append({"role": "assistant", "content": response.content})
                except Exception as e:
                    st.error(f"Error processing request: {str(e)}")
                    st.write("This may be due to API rate limits or invalid API key. Please try again later.")