from setuptools import setup, find_packages

setup(
    name="academic_proofreader",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "python-docx",
        "google-generativeai",
        "python-dotenv",
    ],
    entry_points={
        "console_scripts": [
            "proofread=academic_proofreader.cli:main",
        ],
    },
)
