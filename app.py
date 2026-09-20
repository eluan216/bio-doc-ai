import os

import streamlit as st

from src.styles import apply_custom_css
from src.utils import save_temp_pdf

# Import engine lazily so the UI can still load if LangChain is missing
try:
    from src.engine import get_ai_response
except ImportError as import_err:
    get_ai_response = None
    _import_error = import_err
else:
    _import_error = None

st.set_page_config(page_title="Bio-Doc AI", page_icon="🩺", layout="wide")
apply_custom_css()

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3063/3063176.png", width=100)
    st.title("Settings")
    api_key = os.getenv("OPENAI_API_KEY") or st.text_input(
        "Enter OpenAI API Key",
        type="password",
        help="Get your key at platform.openai.com",
    )
    use_vector_search = st.checkbox(
        "Use FAISS vector search (uses embedding API calls)",
        value=False,
        help="Disable to avoid OpenAI embedding costs on free tier",
    )
    st.caption("Portfolio project · not a medical device")

st.title("🩺 Bio-Doc AI")
st.caption("RAG demo for biomedical PDFs — grounded answers from your documents")

if _import_error is not None:
    st.error(
        "Dependencies are not installed. From the project root run:\n\n"
        "`pip install -r requirements.txt`\n\n"
        f"Details: {_import_error}"
    )
    st.stop()

st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "file_path" not in st.session_state:
    st.session_state.file_path = None

col1, col2 = st.columns([1, 2], gap="large")

with col1:
    st.subheader("📁 Upload Document")
    uploaded_file = st.file_uploader(
        "Upload a Medical PDF", type="pdf", label_visibility="collapsed"
    )

    if uploaded_file and api_key:
        with st.spinner("Preparing document..."):
            file_path = save_temp_pdf(uploaded_file)
            st.session_state.file_path = file_path
            st.success("Document ready")

with col2:
    st.subheader("💬 Ask the document")
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask about the clinical data..."):
        if not api_key:
            st.error("Please enter your OpenAI API key in the sidebar (or set OPENAI_API_KEY).")
        elif not st.session_state.file_path:
            st.error("Please upload a PDF document first.")
        else:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                try:
                    response_text = get_ai_response(
                        st.session_state.file_path,
                        prompt,
                        api_key,
                        use_vector_search=use_vector_search,
                    )
                    st.markdown(response_text)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": response_text}
                    )
                except Exception as e:
                    st.error(f"Error processing request: {e}")
                    st.info(
                        "Check your API key, network access to OpenAI, and that "
                        "`pip install -r requirements.txt` completed successfully. "
                        "You can also turn off FAISS vector search in the sidebar."
                    )
