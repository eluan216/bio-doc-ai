"""Bio-Doc AI - Styles Module
Centralized UI/UX styling and custom CSS components
"""

CUSTOM_CSS = """
    <style>
    /* Global App Background */
    .stApp {
        background: linear-gradient(to right, #ffffff, #f0f7ff);
    }
    
    /* Header Styling */
    h1 {
        color: #1E3A8A; /* Deep Navy Medical Blue */
        font-family: 'Inter', sans-serif;
        font-weight: 800;
    }

    /* Card-like containers for Sidebar */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e0e0e0;
    }

    /* Chat Bubble Styling */
    .stChatMessage {
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 10px;
        box-shadow: 0px 2px 10px rgba(0,0,0,0.05);
    }
    </style>
    """

def apply_theme(st):
    """Apply custom theme to Streamlit app"""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
