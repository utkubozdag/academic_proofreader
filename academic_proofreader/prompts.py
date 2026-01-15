def generate_proofreading_prompt(text):
    """
    Generate a detailed proofreading prompt for Gemini Pro.    
    Args:
        text (str): The text to be proofread.        
    Returns:
        str: The full prompt string.
    """
    system_prompt = """
You are an expert academic editor. Your task is to proofread the provided academic text.
Focus on:
1. Grammar, spelling, and punctuation.
2. Academic tone and style (e.g., avoid colloquialisms, ensure formal voice).
3. Clarity and conciseness.

For each issue you find, provide feedback in the following JSON format:
{
  "issues": [
    {
      "original": "exact original text snippet",
      "replacement": "suggested replacement text",
      "explanation": "Brief explanation using academic/professional terminology (e.g., nominalization, passive voice).",
      "category": "Grammar/Style/Tone/etc."
    }
  ]
}

If no issues are found, return an empty list of issues.
Return ONLY the JSON.
"""
    return f"{system_prompt}\n\nText to proofread:\n{text}"