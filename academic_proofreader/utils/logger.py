import logging
import sys

def setup_logging(level=logging.INFO):
    """
    Setup logging configuration.
    
    Args:
        level (int, optional): Logging level. Defaults to logging.INFO.
        
    Returns:
        logging.Logger: Configured logger.
    """
    logger = logging.getLogger("academic_proofreader")
    logger.setLevel(level)
    
    # Check if handlers are already attached to avoid duplicates
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
    return logger
