# Tech Stack

## Programming Language
- **Python:** The core logic of the CLI tool will be implemented in Python, leveraging its extensive ecosystem for document processing and AI integration.

## Core Libraries
- **python-docx:** Used for reading, writing, and manipulating Microsoft Word (`.docx`) files, specifically for injecting comments and preserving the document structure.
- **google-generativeai:** The official Google SDK for interacting with the Gemini Pro model.
- **python-dotenv:** To manage environment variables and configuration from a `.env` file.

## AI Model
- **Gemini 2.5 Pro:** Utilized for all natural language processing tasks, including error detection, correction, stylistic analysis, and generating the summary report.

## Configuration & Secrets
- **Environment Variables (.env):** API keys and other sensitive configurations will be stored in a local `.env` file. This file will be excluded from version control to ensure security.

## Distribution
- **PIP:** The tool will be packaged for installation via `pip`, making it easy for researchers to install and run in their local Python environments.
