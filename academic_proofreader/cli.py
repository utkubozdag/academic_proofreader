import argparse
import os
import sys
from academic_proofreader.config import load_config
from academic_proofreader.orchestrator import orchestrate
from academic_proofreader.reporter import generate_report
from academic_proofreader.utils.logger import setup_logging

def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="AI-powered Academic Proofreader")
    parser.add_argument("input_file", help="Path to the input .docx file")
    parser.add_argument("--output", "-o", default="output.docx", help="Path to save the proofread .docx file")
    parser.add_argument("--report", "-r", default="report.md", help="Path to save the summary report")
    parser.add_argument("--model", "-m", default="gemini-2.0-flash", help="Gemini model name (default: gemini-2.0-flash)")
    
    args = parser.parse_args()
    
    # Load configuration
    load_config()
    api_key = os.environ.get("GOOGLE_API_KEY")
    
    logger = setup_logging()
    
    if not api_key:
        logger.error("GOOGLE_API_KEY not found in environment variables or .env file.")
        sys.exit(1)
        
    try:
        summary, issues = orchestrate(args.input_file, args.output, api_key, args.model)
        
        # Generate and save report
        report_content = generate_report(summary, issues)
        with open(args.report, "w") as f:
            f.write(report_content)
            
        logger.info(f"Summary report saved to {args.report}")
        logger.info("Proofreading complete!")
        
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
