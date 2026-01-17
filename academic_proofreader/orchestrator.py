import logging
from academic_proofreader.word_processor import WordProcessor
from academic_proofreader.gemini_client import GeminiClient
from academic_proofreader.prompts import generate_proofreading_prompt
from academic_proofreader.parser import parse_feedback
from academic_proofreader.utils.logger import setup_logging

logger = setup_logging()

def orchestrate(input_path, output_path, api_key, model_name="gemini-2.0-flash"):
    """
    Orchestrate the full proofreading flow.
    
    Args:
        input_path (str): Path to the input .docx file.
        output_path (str): Path to save the proofread .docx file.
        api_key (str): Google AI API key.
        model_name (str): Name of the Gemini model to use.
    """
    logger.info(f"Starting proofreading for {input_path}")
    logger.info(f"Using model: {model_name}")
    
    # 1. Initialize components
    processor = WordProcessor(input_path)
    client = GeminiClient(api_key, model_name=model_name)
    
    # 2. Extract text and generate prompt
    text = processor.get_text()
    prompt = generate_proofreading_prompt(text)
    
    # 3. Get feedback from Gemini
    logger.info("Sending text to Gemini for analysis...")
    raw_response = client.generate(prompt)
    
    # 4. Parse feedback
    summary, issues = parse_feedback(raw_response)
    logger.info(f"Found {len(issues)} issues.")
    
    # 5. Apply tracked changes (revisions)
    applied_count = 0
    for issue in issues:
        original = issue.get("original")
        replacement = issue.get("replacement")
        
        if original and replacement:
            if processor.add_tracked_change(original, replacement, author="Academic Proofreader"):
                applied_count += 1
                logger.debug(f"Applied change: '{original}' -> '{replacement}'")
            else:
                logger.warning(f"Could not find text to change: '{original}'")
    
    logger.info(f"Applied {applied_count} of {len(issues)} tracked changes.")
    
    # 6. Enable track revisions mode so Word shows the changes
    processor.enable_track_revisions()
    
    # 7. Save document
    processor.save(output_path)
    logger.info(f"Saved proofread document to {output_path}")
    
    return summary, issues  # Return both for report generation

