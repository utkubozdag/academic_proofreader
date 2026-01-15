import os
from dotenv import load_dotenv

def load_config(dotenv_path=None):
    """
    Load environment variables from .env file.
    
    Args:
        dotenv_path (str, optional): Path to .env file. Defaults to None (auto-discovery).
    """
    load_dotenv(dotenv_path=dotenv_path)
