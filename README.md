# Academic Proofreader

AI-powered proofreading for academic documents. Uses Google Gemini to analyze your Word documents and applies corrections as **Track Changes** you can accept or reject.

## Features

- ✏️ **Track Changes** - Corrections appear as Word revisions (accept/reject individually)
- 📊 **Summary Report** - High-level feedback on document quality
- 🎯 **Academic Focus** - Tuned for academic writing style
- ⚡ **Fast** - Visual progress with spinner animations

## Setup

```bash
# Clone and install
git clone https://github.com/utkubozdag/academic_proofreader.git
cd academic_proofreader
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .

# Configure API key
echo "GOOGLE_API_KEY=your_key_here" > .env
```

Get your API key at [Google AI Studio](https://aistudio.google.com/apikey).

## Usage

```bash
proofreader document.docx
```

**Options:**
| Flag | Description | Default |
|------|-------------|---------|
| `-o` | Output file | `output.docx` |
| `-r` | Report file | `report.docx` |
| `-m` | Model name | `gemini-2.0-flash` |

**Example:**
```bash
proofreader thesis.docx -o thesis_reviewed.docx -m gemini-2.5-pro
```

## Output

1. **Proofread document** (`output.docx`) - Open in Word, use Review tab to accept/reject changes
2. **Summary report** (`report.docx`) - Overall assessment, strengths, areas for improvement

## License

MIT
