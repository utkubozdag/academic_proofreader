import logging
from academic_proofreader.word_processor import WordProcessor
from academic_proofreader.gemini_client import GeminiClient
from academic_proofreader.prompts import generate_proofreading_prompt
from academic_proofreader.parser import parse_feedback
from academic_proofreader.utils.logger import setup_logging

logger = setup_logging()

def orchestrate(input_path, output_path, api_key):
    """
    Orchestrate the full proofreading flow.
    
    Args:
        input_path (str): Path to the input .docx file.
        output_path (str): Path to save the proofread .docx file.
        api_key (str): Google AI API key.
    """
    logger.info(f"Starting proofreading for {input_path}")
    
    # 1. Initialize components
    processor = WordProcessor(input_path)
    client = GeminiClient(api_key)
    
    # 2. Extract text and generate prompt
    text = processor.get_text()
    prompt = generate_proofreading_prompt(text)
    
    # 3. Get feedback from Gemini
    logger.info("Sending text to Gemini for analysis...")
    raw_response = client.generate(prompt)
    
    # 4. Parse feedback
    issues = parse_feedback(raw_response)
    logger.info(f"Found {len(issues)} issues.")
    
    # 5. Inject comments
    # Simple mapping: find paragraph index by matching text
    # In a real app, this might need more robust matching (e.g., fuzzy or context-aware)
    for issue in issues:
        original = issue.get("original")
        comment_text = f"Suggested: {issue.get('replacement')}\n\n{issue.get('explanation')}"
        
        # Find the paragraph
        for i, para in enumerate(processor.doc.paragraphs):
            if original in para.text:
                processor.add_comment(i, comment_text, author="Academic Proofreader")
                break
    
    # 6. Save document
    processor.save(output_path)
    logger.info(f"Saved proofread document to {output_path}")
    
    return issues # Return issues for report generation later
