import pytest
import sys
from unittest.mock import patch, MagicMock
from academic_proofreader.cli import main

def test_cli_arguments():
    """Test that CLI parses arguments correctly."""
    with patch('sys.argv', ['proofreader', 'input.docx', '--output', 'out.docx', '--report', 'report.docx']):
        with patch('academic_proofreader.cli.orchestrate') as mock_orchestrate:
            with patch('academic_proofreader.cli.generate_report') as mock_gen_report:
                with patch('academic_proofreader.cli.save_report') as mock_save_report:
                    mock_orchestrate.return_value = ({}, [])  # (summary, issues) tuple
                    mock_doc = MagicMock()
                    mock_gen_report.return_value = mock_doc
                    
                    # Mock config loading
                    with patch('academic_proofreader.cli.load_config'):
                        # Mock os.environ.get for API key
                        with patch('os.environ.get', return_value="fake_key"):
                            main()
                            
                            mock_orchestrate.assert_called_once_with('input.docx', 'out.docx', 'fake_key', 'gemini-2.0-flash')
                            mock_gen_report.assert_called_once_with({}, [])
                            mock_save_report.assert_called_once_with(mock_doc, 'report.docx')


def test_cli_missing_api_key():
    """Test that CLI exits if API key is missing."""
    with patch('sys.argv', ['proofread', 'input.docx']):
        with patch('academic_proofreader.cli.load_config'):
            with patch('os.environ.get', return_value=None):
                with pytest.raises(SystemExit):
                    main()