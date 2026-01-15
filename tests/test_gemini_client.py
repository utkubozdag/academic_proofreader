import pytest
from unittest.mock import patch, MagicMock
from academic_proofreader.gemini_client import GeminiClient

@patch('google.generativeai.GenerativeModel')
@patch('google.generativeai.configure')
def test_gemini_client_init(mock_configure, mock_model):
    """Test that GeminiClient initializes correctly."""
    client = GeminiClient(api_key="test_key")
    
    mock_configure.assert_called_once_with(api_key="test_key")
    mock_model.assert_called_once_with(model_name="gemini-2.0-flash")

@patch('google.generativeai.GenerativeModel')
@patch('google.generativeai.configure')
def test_gemini_client_generate(mock_configure, mock_model):
    """Test that GeminiClient can generate text."""
    mock_response = MagicMock()
    mock_response.text = "Proofread text"
    mock_instance = mock_model.return_value
    mock_instance.generate_content.return_value = mock_response
    
    client = GeminiClient(api_key="test_key")
    response = client.generate("Input text")
    
    assert response == "Proofread text"
    mock_instance.generate_content.assert_called_once_with("Input text")
