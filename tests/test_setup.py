import os

def test_project_structure():
    """Test that the project structure is initialized."""
    assert os.path.exists("setup.py")
    assert os.path.exists("requirements.txt")
    assert os.path.exists("academic_proofreader")
    assert os.path.exists("academic_proofreader/__init__.py")