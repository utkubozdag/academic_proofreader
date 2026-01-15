import pytest
from academic_proofreader.reporter import generate_report

def test_generate_report():
    """Test generating a summary report."""
    issues = [
        {"category": "Grammar", "explanation": "E1"},
        {"category": "Style", "explanation": "E2"},
        {"category": "Grammar", "explanation": "E3"}
    ]
    
    report = generate_report(issues)
    
    assert "# Proofreading Summary Report" in report
    assert "Total Issues Found: 3" in report
    assert "Grammar" in report
    assert "Style" in report
    # Check for counts in report
    assert "Grammar: 2" in report
    assert "Style: 1" in report
