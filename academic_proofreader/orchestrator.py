import logging
import sys
import threading
import time
from academic_proofreader.word_processor import WordProcessor
from academic_proofreader.gemini_client import GeminiClient
from academic_proofreader.prompts import generate_proofreading_prompt
from academic_proofreader.parser import parse_feedback
from academic_proofreader.utils.logger import setup_logging

logger = setup_logging()


class Spinner:
    """A simple CLI spinner for visual feedback."""
    
    def __init__(self, message="Processing"):
        self.spinner_chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        self.message = message
        self.running = False
        self.thread = None
    
    def spin(self):
        idx = 0
        while self.running:
            sys.stdout.write(f"\r{self.spinner_chars[idx]} {self.message}")
            sys.stdout.flush()
            idx = (idx + 1) % len(self.spinner_chars)
            time.sleep(0.1)
    
    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self.spin, daemon=True)
        self.thread.start()
    
    def stop(self, success=True):
        self.running = False
        if self.thread:
            self.thread.join(timeout=0.5)
        icon = "✓" if success else "✗"
        sys.stdout.write(f"\r{icon} {self.message}\n")
        sys.stdout.flush()


def print_step(icon, message):
    """Print a step with an icon."""
    print(f"{icon} {message}")


def orchestrate(input_path, output_path, api_key, model_name="gemini-2.0-flash"):
    """
    Orchestrate the full proofreading flow.
    
    Args:
        input_path (str): Path to the input .docx file.
        output_path (str): Path to save the proofread .docx file.
        api_key (str): Google AI API key.
        model_name (str): Name of the Gemini model to use.
    """
    print()
    print("━" * 50)
    print("  📝 Academic Proofreader")
    print("━" * 50)
    print()
    
    # 1. Initialize components
    print_step("📄", f"Loading document: {input_path}")
    processor = WordProcessor(input_path)
    client = GeminiClient(api_key, model_name=model_name)
    
    # 2. Extract text
    print_step("📖", "Extracting text from document...")
    text = processor.get_text()
    word_count = len(text.split())
    print_step("   ", f"Found {word_count} words")
    
    # 3. Generate prompt
    prompt = generate_proofreading_prompt(text)
    
    # 4. Get feedback from Gemini with spinner
    spinner = Spinner(f"Analyzing with {model_name}...")
    spinner.start()
    
    try:
        raw_response = client.generate(prompt)
        spinner.stop(success=True)
    except Exception as e:
        spinner.stop(success=False)
        raise e
    
    # 5. Parse feedback
    summary, issues = parse_feedback(raw_response)
    print_step("🔍", f"Found {len(issues)} issues to address")
    
    # 6. Apply tracked changes
    if issues:
        spinner = Spinner("Applying tracked changes...")
        spinner.start()
        
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
        
        spinner.stop(success=True)
        print_step("   ", f"Applied {applied_count} of {len(issues)} changes")
    
    # 7. Enable track revisions
    processor.enable_track_revisions()
    
    # 8. Save document
    processor.save(output_path)
    print_step("💾", f"Saved proofread document: {output_path}")
    
    print()
    print("━" * 50)
    print("  ✨ Proofreading complete!")
    print("━" * 50)
    print()
    
    return summary, issues


