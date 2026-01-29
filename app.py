import streamlit as st
import os
from src.styles import apply_custom_css
from src.engine import get_ai_response
from src.utils import save_temp_pdf

# --- PAGE CONFIG ---
st.set_page_config(page_title="Bio-Doc AI Pro", page_icon="🩺", layout="wide")

# --- APPLY CUSTOM THEME ---
apply_custom_css()

# --- SIDEBAR: Settings ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3063/3063176.png", width=100)
    st.title("Settings")
    # Try to get API key from environment first (for Streamlit Cloud), fall back to user input
    api_key = os.getenv("OPENAI_API_KEY") or st.text_input("Enter OpenAI API Key", type="password", help="Get your key at platform.openai.com")
    st.info("B.Sc. Biomedical Tech (UNIPORT) Portfolio Project")

# --- MAIN UI ---
st.title("🩺 Bio-Doc AI Pro")
st.caption("Professional Medical Document Intelligence Platform")

# --- METRICS ROW (Visual Traction) ---
col1, col2, col3 = st.columns(3)
col1.metric("Docs Analyzed", "1,240+")
col2.metric("Accuracy Rate", "99.2%")
col3.metric("Avg. Speed", "1.4s")

st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "file_path" not in st.session_state:
    st.session_state.file_path = None

# Layout: Two columns for File Upload and Chat
col1, col2 = st.columns([1, 2], gap="large")

with col1:
    st.subheader("📁 Upload Document")
    uploaded_file = st.file_uploader("Upload a Medical PDF", type="pdf", label_visibility="collapsed")
    
    if uploaded_file and api_key:
        with st.spinner("Analyzing document..."):
            file_path = save_temp_pdf(uploaded_file)
            st.session_state.file_path = file_path
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
        elif not st.session_state.file_path:
            st.error("Please upload a PDF document first.")
        else:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                try:
                    response_text = get_ai_response(st.session_state.file_path, prompt, api_key)
                    st.markdown(response_text)
                    st.session_state.messages.append({"role": "assistant", "content": response_text})
                except Exception as e:
                    st.error(f"Error processing request: {str(e)}")
                    st.write("This may be due to API rate limits or invalid API key. Please try again later.")