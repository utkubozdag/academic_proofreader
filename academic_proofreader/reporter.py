from collections import Counter

def generate_report(summary, issues):
    """
    Generate a high-level Markdown summary report of the proofreading findings.
    
    Args:
        summary (dict): High-level summary from the model.
        issues (list): List of issue dictionaries.
        
    Returns:
        str: The Markdown report.
    """
    lines = ["# Proofreading Summary Report\n"]
    
    # Overall Assessment
    if summary.get("overall_assessment"):
        lines.append("## Overall Assessment\n")
        lines.append(summary["overall_assessment"])
        lines.append("")
    
    # Strengths
    if summary.get("strengths"):
        lines.append("## Strengths\n")
        for strength in summary["strengths"]:
            lines.append(f"- {strength}")
        lines.append("")
    
    # Areas for Improvement
    if summary.get("areas_for_improvement"):
        lines.append("## Areas for Improvement\n")
        for area in summary["areas_for_improvement"]:
            lines.append(f"- {area}")
        lines.append("")
    
    # Section-level Feedback
    if summary.get("sections"):
        lines.append("## Section Feedback\n")
        for section in summary["sections"]:
            name = section.get("name", "Untitled")
            feedback = section.get("feedback", "No specific feedback.")
            lines.append(f"### {name}\n")
            lines.append(feedback)
            lines.append("")
    
    # Statistics
    if issues:
        lines.append("## Correction Statistics\n")
        total = len(issues)
        categories = [issue.get("category", "Other") for issue in issues]
        category_counts = Counter(categories)
        
        lines.append(f"**Total corrections applied: {total}**\n")
        lines.append("By category:")
        for cat, count in sorted(category_counts.items()):
            lines.append(f"- {cat}: {count}")
        lines.append("")
        lines.append("*See the tracked changes in the output document for detailed corrections.*")
    else:
        lines.append("## Corrections\n")
        lines.append("No corrections needed. Great job!")
    
    return "\n".join(lines)

