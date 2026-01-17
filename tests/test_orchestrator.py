import pytest
from unittest.mock import MagicMock, patch
from academic_proofreader.orchestrator import orchestrate

@patch('academic_proofreader.orchestrator.WordProcessor')
@patch('academic_proofreader.orchestrator.GeminiClient')
@patch('academic_proofreader.orchestrator.generate_proofreading_prompt')
@patch('academic_proofreader.orchestrator.parse_feedback')
def test_orchestrate(mock_parse, mock_prompt, mock_client_cls, mock_processor_cls):
    """Test the full orchestration flow."""
    # Setup mocks
    mock_processor = mock_processor_cls.return_value
    mock_processor.get_text.return_value = "Paragraph 1\nParagraph 2"
    
    p1 = MagicMock()
    p1.text = "Paragraph 1"
    p2 = MagicMock()
    p2.text = "Paragraph 2"
    mock_processor.doc.paragraphs = [p1, p2]
    
    mock_client = mock_client_cls.return_value
    mock_client.generate.return_value = "Gemini Response"
    
    mock_prompt.return_value = "Full Prompt"
    
    # Simulate finding one issue in the first paragraph
    mock_parse.return_value = [
        {
            "original": "Paragraph 1",
            "replacement": "Better Paragraph 1",
            "explanation": "Fixed.",
            "category": "Grammar"
        }
    ]
    
    orchestrate("input.docx", "output.docx", "api_key")
    
    # Verify flow
    mock_processor_cls.assert_called_once_with("input.docx")
    mock_client_cls.assert_called_once_with("api_key")
    mock_processor.get_text.assert_called_once()
    mock_prompt.assert_called_once_with("Paragraph 1\nParagraph 2")
    mock_client.generate.assert_called_once_with("Full Prompt")
    mock_parse.assert_called_once_with("Gemini Response")
    
    # Verify tracked change injection (one issue found)
    mock_processor.add_tracked_change.assert_called_once()
    mock_processor.enable_track_revisions.assert_called_once()
    mock_processor.save.assert_called_once_with("output.docx")

