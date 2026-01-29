"""
Bio-Doc AI - Test Suite
Automated tests for engine, utils, and core functionality
"""

import pytest
import os
from pathlib import Path
from src.engine import load_pdf, initialize_llm, query_document
from src.utils import validate_api_key, save_temp_pdf


class TestAPIKeyValidation:
    """Tests for API key validation"""
    
    def test_valid_api_key(self):
        """Test that valid API key passes validation"""
        valid_key = "sk-" + "a" * 45  # Realistic OpenAI key format
        assert validate_api_key(valid_key) == True
    
    def test_empty_api_key(self):
        """Test that empty API key fails validation"""
        assert validate_api_key("") == False
    
    def test_short_api_key(self):
        """Test that short API key fails validation"""
        assert validate_api_key("short") == False


class TestEngineInitialization:
    """Tests for LLM engine initialization"""
    
    def test_llm_initialization_with_api_key(self):
        """Test that LLM can be initialized with valid API key"""
        api_key = "sk-" + "a" * 45
        try:
            llm = initialize_llm(api_key)
            assert llm is not None
            assert llm.model_name == "gpt-4o-mini"
        except Exception as e:
            # Skip if API key validation fails at OpenAI level
            pytest.skip(f"OpenAI API validation failed: {str(e)}")


class TestDocumentProcessing:
    """Tests for PDF document processing"""
    
    @pytest.fixture
    def sample_pdf_path(self):
        """Create a temporary test PDF"""
        # This would normally create a test PDF
        # For now, we'll skip if no sample file exists
        sample_dir = Path("data/samples")
        if sample_dir.exists() and list(sample_dir.glob("*.pdf")):
            return list(sample_dir.glob("*.pdf"))[0]
        return None
    
    def test_pdf_loading_with_sample(self, sample_pdf_path):
        """Test PDF loading with actual sample file"""
        if sample_pdf_path is None:
            pytest.skip("No sample PDF available in data/samples/")
        
        try:
            context = load_pdf(str(sample_pdf_path), max_pages=2)
            assert context is not None
            assert len(context) > 0
            assert isinstance(context, str)
        except Exception as e:
            pytest.fail(f"PDF loading failed: {str(e)}")


class TestUtilityFunctions:
    """Tests for utility functions"""
    
    def test_validate_api_key_format(self):
        """Test API key format validation"""
        # Valid OpenAI format
        valid = "sk-" + "x" * 45
        assert validate_api_key(valid) == True
        
        # Invalid format
        invalid = "invalid-key"
        assert validate_api_key(invalid) == False


def test_project_structure():
    """Test that essential project files exist"""
    required_files = [
        "app.py",
        "requirements.txt",
        "README.md",
        "src/__init__.py",
        "src/engine.py",
        "src/styles.py",
        "src/utils.py",
        ".streamlit/config.toml"
    ]
    
    for file_path in required_files:
        assert Path(file_path).exists(), f"Missing required file: {file_path}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
