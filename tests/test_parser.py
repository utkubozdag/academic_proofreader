import pytest
from academic_proofreader.parser import parse_feedback

def test_parse_valid_json():
    """Test parsing a valid JSON response."""
    response = '{"summary": {"overall_assessment": "Good"}, "issues": [{"original": "bad", "replacement": "good", "explanation": "fix", "category": "G"}]}'
    summary, issues = parse_feedback(response)
    
    assert len(issues) == 1
    assert issues[0]['original'] == "bad"
    assert summary['overall_assessment'] == "Good"

def test_parse_json_with_markdown():
    """Test parsing JSON wrapped in markdown code blocks."""
    response = """```json
{"summary": {}, "issues": [{"original": "bad", "replacement": "good", "explanation": "fix", "category": "G"}]}
```"""
    summary, issues = parse_feedback(response)
    
    assert len(issues) == 1
    assert issues[0]['original'] == "bad"

def test_parse_invalid_json():
    """Test parsing invalid JSON."""
    response = "Not a JSON"
    with pytest.raises(ValueError, match="Failed to parse Gemini response as JSON"):
        parse_feedback(response)