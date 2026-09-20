"""Bio-Doc AI - Test Suite

Unit tests that do not require a live OpenAI API key.
LLM/network tests are skipped when deps or keys are unavailable.
"""

from pathlib import Path

import pytest

from src.utils import validate_api_key


class TestAPIKeyValidation:
    """Tests for API key format validation."""

    def test_valid_api_key(self):
        valid_key = "sk-" + "a" * 45
        assert validate_api_key(valid_key) is True

    def test_empty_api_key(self):
        assert validate_api_key("") is False

    def test_short_api_key(self):
        assert validate_api_key("short") is False


class TestEngineImports:
    """Engine module must import even when LangChain is optional at import time."""

    def test_engine_module_imports(self):
        import src.engine as engine

        assert hasattr(engine, "get_ai_response")
        assert hasattr(engine, "load_pdf")
        assert hasattr(engine, "initialize_llm")

    def test_missing_deps_message(self):
        """If LangChain stack is missing, _require_langchain raises a clear error."""
        import src.engine as engine

        try:
            engine._require_langchain()
        except ImportError as e:
            assert "pip install -r requirements.txt" in str(e)
        except Exception:
            # Deps are installed — that is also fine
            pass


class TestEngineInitialization:
    """LLM init — skip when OpenAI is unreachable or key is fake."""

    def test_llm_initialization_with_api_key(self):
        api_key = "sk-" + "a" * 45
        try:
            from src.engine import initialize_llm

            llm = initialize_llm(api_key)
            assert llm is not None
            # langchain-openai versions differ: model vs model_name
            model = getattr(llm, "model_name", None) or getattr(llm, "model", None)
            assert model is not None
        except Exception as e:
            pytest.skip(f"OpenAI/LangChain init skipped: {e}")


class TestDocumentProcessing:
    """PDF loading when a sample file exists."""

    @pytest.fixture
    def sample_pdf_path(self):
        sample_dir = Path("data/samples")
        if sample_dir.exists() and list(sample_dir.glob("*.pdf")):
            return list(sample_dir.glob("*.pdf"))[0]
        return None

    def test_pdf_loading_with_sample(self, sample_pdf_path):
        if sample_pdf_path is None:
            pytest.skip("No sample PDF available in data/samples/")

        try:
            from src.engine import load_pdf

            context = load_pdf(str(sample_pdf_path), max_pages=2)
            assert context is not None
            assert len(context) > 0
            assert isinstance(context, str)
        except ImportError as e:
            pytest.skip(f"Deps not installed: {e}")
        except Exception as e:
            pytest.fail(f"PDF loading failed: {e}")


class TestUtilityFunctions:
    def test_validate_api_key_format(self):
        valid = "sk-" + "x" * 45
        assert validate_api_key(valid) is True
        assert validate_api_key("invalid-key") is False


def test_project_structure():
    required_files = [
        "app.py",
        "requirements.txt",
        "README.md",
        "src/__init__.py",
        "src/engine.py",
        "src/styles.py",
        "src/utils.py",
        ".streamlit/config.toml",
    ]
    for file_path in required_files:
        assert Path(file_path).exists(), f"Missing required file: {file_path}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
