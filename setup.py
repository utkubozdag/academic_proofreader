from setuptools import setup, find_packages

setup(
    name="academic_proofreader",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "python-docx",
        "google-genai",
        "python-dotenv",
    ],
    entry_points={
        "console_scripts": [
            "proofreader=academic_proofreader.cli:main",
        ],
    },
)
