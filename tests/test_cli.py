import pytest
import sys
from unittest.mock import patch, mock_open
from academic_proofreader.cli import main

def test_cli_arguments():
    """Test that CLI parses arguments correctly."""
    with patch('sys.argv', ['proofread', 'input.docx', '--output', 'out.docx', '--report', 'report.md']):
        with patch('academic_proofreader.cli.orchestrate') as mock_orchestrate:
            with patch('academic_proofreader.cli.generate_report') as mock_report:
                mock_orchestrate.return_value = []
                mock_report.return_value = "Mock Report Content"
                
                # Mock config loading
                with patch('academic_proofreader.cli.load_config'):
                    # Mock os.environ.get for API key
                    with patch('os.environ.get', return_value="fake_key"):
                        # Mock file writing
                        with patch('builtins.open', mock_open()) as mock_file:
                            main()
                            
                            mock_orchestrate.assert_called_once_with('input.docx', 'out.docx', 'fake_key')
                            mock_report.assert_called_once()
                            mock_file.assert_called_with('report.md', 'w')
                            mock_file().write.assert_called_with("Mock Report Content")

def test_cli_missing_api_key():
    """Test that CLI exits if API key is missing."""
    with patch('sys.argv', ['proofread', 'input.docx']):
        with patch('academic_proofreader.cli.load_config'):
            with patch('os.environ.get', return_value=None):
                with pytest.raises(SystemExit):
                    main()