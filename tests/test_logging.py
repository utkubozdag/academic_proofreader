import logging
import pytest
from academic_proofreader.utils.logger import setup_logging

def test_setup_logging():
    """Test that logging is set up correctly."""
    logger = setup_logging()
    
    assert logger.name == "academic_proofreader"
    assert logger.level == logging.INFO
    assert len(logger.handlers) > 0
    assert isinstance(logger.handlers[0], logging.StreamHandler)
