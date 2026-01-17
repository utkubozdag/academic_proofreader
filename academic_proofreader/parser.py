import json
import re

def parse_feedback(raw_response):
    """
    Parse the JSON response from Gemini Pro.
    
    Args:
        raw_response (str): The raw string response from the model.
        
    Returns:
        tuple: (summary dict, list of issue dicts)
        
    Raises:
        ValueError: If the response cannot be parsed as JSON.
    """
    # Remove markdown code blocks if present
    cleaned_response = re.sub(r'```json\s*|\s*```', '', raw_response).strip()
    
    try:
        data = json.loads(cleaned_response)
        summary = data.get("summary", {})
        issues = data.get("issues", [])
        return summary, issues
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse Gemini response as JSON: {e}\nRaw: {raw_response}")


