import pytest
from academic_proofreader.prompts import generate_proofreading_prompt

def test_generate_proofreading_prompt():
    """Test that the proofreading prompt is generated correctly."""
    text = "This is a sample academic text."
    prompt = generate_proofreading_prompt(text)
    
    assert text in prompt
    assert "academic" in prompt.lower()
    assert "grammar" in prompt.lower()
    assert "tone" in prompt.lower()
    assert "JSON" in prompt  # We want structured output for easier parsing
