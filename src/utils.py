"""Bio-Doc AI - Utilities Module
File handling and compliance utilities
"""

import os
from pathlib import Path


def save_temp_pdf(uploaded_file) -> str:
    """Safely save uploaded PDF to temporary file"""
    temp_path = "temp.pdf"
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return temp_path


def cleanup_temp_file(file_path: str = "temp.pdf") -> None:
    """Remove temporary PDF file"""
    if os.path.exists(file_path):
        os.remove(file_path)


def validate_api_key(api_key: str) -> bool:
    """Validate API key format (basic check)"""
    return bool(api_key and len(api_key) > 20)
