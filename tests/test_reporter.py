import pytest
from academic_proofreader.reporter import generate_report

def test_generate_report():
    """Test generating a summary report."""
    summary = {
        "overall_assessment": "The document is well-written.",
        "strengths": ["Clear structure", "Good vocabulary"],
        "areas_for_improvement": ["Minor grammar issues"]
    }
    issues = [
        {"category": "Grammar", "explanation": "E1"},
        {"category": "Style", "explanation": "E2"},
        {"category": "Grammar", "explanation": "E3"}
    ]
    
    report = generate_report(summary, issues)
    
    assert "# Proofreading Summary Report" in report
    assert "Overall Assessment" in report
    assert "well-written" in report
    assert "Strengths" in report
    assert "Areas for Improvement" in report
    assert "Total corrections applied: 3" in report
    assert "Grammar: 2" in report
    assert "Style: 1" in report

