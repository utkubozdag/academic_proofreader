import pytest
from academic_proofreader.parser import parse_feedback

def test_parse_valid_json():
    """Test parsing a valid JSON response."""
    response = '{"issues": [{"original": "bad", "replacement": "good", "explanation": "fix", "category": "G"}]}'
    result = parse_feedback(response)
    
    assert len(result) == 1
    assert result[0]['original'] == "bad"

def test_parse_json_with_markdown():
    """Test parsing JSON wrapped in markdown code blocks."""
    response = """```json
{"issues": [{"original": "bad", "replacement": "good", "explanation": "fix", "category": "G"}]}
```"""
    result = parse_feedback(response)
    
    assert len(result) == 1
    assert result[0]['original'] == "bad"

def test_parse_invalid_json():
    """Test parsing invalid JSON."""
    response = "Not a JSON"
    with pytest.raises(ValueError, match="Failed to parse Gemini response as JSON"):
        parse_feedback(response)