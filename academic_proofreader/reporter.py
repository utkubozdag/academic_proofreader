from collections import Counter

def generate_report(issues):
    """
    Generate a Markdown summary report of the proofreading findings.
    
    Args:
        issues (list): List of issue dictionaries.
        
    Returns:
        str: The Markdown report.
    """
    if not issues:
        return "# Proofreading Summary Report\n\nNo issues found! Great job."
        
    total_issues = len(issues)
    categories = [issue.get("category", "Other") for issue in issues]
    category_counts = Counter(categories)
    
    lines = [
        "# Proofreading Summary Report",
        f"\n**Total Issues Found: {total_issues}**\n",
        "## Issues by Category"
    ]
    
    for cat, count in category_counts.items():
        lines.append(f"- {cat}: {count}")
        
    lines.append("\n## Detailed Findings")
    
    for cat in sorted(category_counts.keys()):
        lines.append(f"\n### {cat}")
        cat_issues = [i for i in issues if i.get("category", "Other") == cat]
        for i, issue in enumerate(cat_issues, 1):
            lines.append(f"{i}. **{issue.get('original')}** -> *{issue.get('replacement')}*")
            lines.append(f"   - {issue.get('explanation')}")
            
    return "\n".join(lines)
