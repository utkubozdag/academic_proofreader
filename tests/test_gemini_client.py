import pytest
from unittest.mock import patch, MagicMock
from academic_proofreader.gemini_client import GeminiClient

@patch('academic_proofreader.gemini_client.genai.Client')
def test_gemini_client_init(mock_client_cls):
    """Test that GeminiClient initializes correctly."""
    client = GeminiClient(api_key="test_key")
    
    mock_client_cls.assert_called_once_with(api_key="test_key")
    assert client.model_name == "gemini-2.0-flash"

@patch('academic_proofreader.gemini_client.genai.Client')
def test_gemini_client_generate(mock_client_cls):
    """Test that GeminiClient can generate text."""
    mock_response = MagicMock()
    mock_response.text = "Proofread text"
    mock_client = mock_client_cls.return_value
    mock_client.models.generate_content.return_value = mock_response
    
    client = GeminiClient(api_key="test_key", model_name="gemini-2.0-flash")
    response = client.generate("Input text")
    
    assert response == "Proofread text"
    mock_client.models.generate_content.assert_called_once_with(
        model="gemini-2.0-flash",
        contents="Input text"
    )

