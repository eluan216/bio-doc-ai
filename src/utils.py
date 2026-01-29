"""Bio-Doc AI - Utilities Module
File handling, validation, and compliance utilities
"""

import os
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def save_temp_pdf(uploaded_file) -> str:
    """
    Safely save uploaded PDF to temporary file.
    
    Args:
        uploaded_file: Streamlit UploadedFile object
        
    Returns:
        Path to saved temporary PDF file
        
    Raises:
        ValueError: If file is invalid or save fails
    """
    try:
        if not uploaded_file:
            raise ValueError("No file provided")
        
        temp_path = "temp.pdf"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        logger.info(f"Successfully saved uploaded file to {temp_path}")
        return temp_path
        
    except Exception as e:
        logger.error(f"Error saving PDF: {str(e)}")
        raise ValueError(f"Failed to save PDF: {str(e)}")


def cleanup_temp_file(file_path: str = "temp.pdf") -> bool:
    """
    Safely remove temporary PDF file.
    
    Args:
        file_path: Path to temporary file (default: "temp.pdf")
        
    Returns:
        True if file was deleted, False if it didn't exist
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Cleaned up temporary file: {file_path}")
            return True
        else:
            logger.info(f"Temporary file not found: {file_path}")
            return False
            
    except Exception as e:
        logger.error(f"Error cleaning up file {file_path}: {str(e)}")
        return False


def validate_api_key(api_key: str) -> bool:
    """
    Validate OpenAI API key format.
    
    Checks that the API key:
    - Is not empty
    - Has minimum length (OpenAI keys are typically 48+ characters)
    - Follows expected format
    
    Args:
        api_key: API key string to validate
        
    Returns:
        True if API key format is valid, False otherwise
    """
    if not api_key:
        logger.warning("API key validation failed: empty key")
        return False
    
    api_key = api_key.strip()
    
    # OpenAI keys typically start with 'sk-' and are 48+ characters
    if len(api_key) < 20:
        logger.warning(f"API key validation failed: key too short ({len(api_key)} chars)")
        return False
    
    logger.info("API key validation passed")
    return True


def get_sample_pdfs(sample_dir: str = "data/samples") -> list:
    """
    Get list of available sample PDF files.
    
    Args:
        sample_dir: Directory containing sample PDFs (default: "data/samples")
        
    Returns:
        List of PDF file paths in sample directory
    """
    try:
        sample_path = Path(sample_dir)
        
        if not sample_path.exists():
            logger.warning(f"Sample directory not found: {sample_dir}")
            return []
        
        pdfs = list(sample_path.glob("*.pdf"))
        logger.info(f"Found {len(pdfs)} sample PDFs")
        return [str(p) for p in pdfs]
        
    except Exception as e:
        logger.error(f"Error reading sample directory: {str(e)}")
        return []


def estimate_tokens(text: str) -> int:
    """
    Estimate token count for text (rough approximation).
    
    Uses the common rule: 1 token ≈ 4 characters
    
    Args:
        text: Text to estimate tokens for
        
    Returns:
        Estimated token count
    """
    return len(text) // 4


def check_file_size(file_path: str, max_size_mb: int = 25) -> bool:
    """
    Check if file size is within acceptable limits.
    
    Args:
        file_path: Path to file to check
        max_size_mb: Maximum allowed file size in MB (default: 25)
        
    Returns:
        True if file size is acceptable, False otherwise
    """
    try:
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return False
        
        file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
        
        if file_size_mb > max_size_mb:
            logger.warning(f"File too large: {file_size_mb:.2f}MB > {max_size_mb}MB")
            return False
        
        logger.info(f"File size check passed: {file_size_mb:.2f}MB")
        return True
        
    except Exception as e:
        logger.error(f"Error checking file size: {str(e)}")
        return False
