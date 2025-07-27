markdown# PDF Document Analyzer

A Python application that extracts and analyzes sections from PDF documents using semantic similarity matching. The tool processes PDF collections based on specific personas and tasks, ranking content by relevance using sentence transformers and cosine similarity.

## Features

- **PDF Text Extraction**: Extracts text content from PDF documents using PyMuPDF
- **Section Detection**: Automatically identifies document sections based on formatting patterns
- **Semantic Analysis**: Uses sentence transformers to embed text and compute semantic similarity
- **Content Ranking**: Ranks sections and sentences by relevance to specified persona and task
- **Batch Processing**: Processes multiple document collections automatically
- **JSON Output**: Generates structured output with metadata and analysis results

## Requirements

### Python Dependencies

```
PyMuPDF (fitz)
sentence-transformers
scikit-learn
spacy
```

### System Requirements

- Python 3.7+
- Docker (for containerized execution)
- Sufficient memory for sentence transformer models

## Installation

1. Clone the repository
2. Install Python dependencies:
   ```bash
   pip install PyMuPDF sentence-transformers scikit-learn spacy
   ```
3. Download spaCy language model (if needed):
   ```bash
   python -m spacy download en_core_web_sm
   ```

## Usage

### Input Structure

The application expects the following directory structure:

```
input/
├── collection1/
│   ├── challenge1b_input.json
│   └── PDFs/
│       ├── document1.pdf
│       └── document2.pdf
└── collection2/
    ├── challenge1b_input.json
    └── PDFs/
        └── document3.pdf
```

### Input JSON Format

Each `challenge1b_input.json` should contain:

```json
{
  "persona": {
    "role": "Data Scientist analyzing market trends"
  },
  "job_to_be_done": {
    "task": "Extract key insights about consumer behavior"
  },
  "documents": [
    {
      "filename": "document1.pdf"
    },
    {
      "filename": "document2.pdf"
    }
  ]
}
```

### Command Line Execution

**Process all collections:**
```bash
python main.py
```

**Process specific collection:**
```bash
python main.py collection_name
```

### Docker Execution

**Build the Docker image:**
```bash
docker build --platform linux/amd64 -t adobe1b:localtest .
```

**Run the container:**
```bash
docker run --rm \
  -v "${PWD}:/app/input" \
  --network none \
  adobe1b:localtest
```

**Windows PowerShell:**
```powershell
docker run --rm `
  -v "${PWD}:/app/input" `
  --network none `
  adobe1b:localtest
```

## Output Format

The application generates `challenge1b_output.json` with the following structure:

```json
{
  "metadata": {
    "input_documents": ["document1.pdf", "document2.pdf"],
    "persona": "Data Scientist analyzing market trends",
    "job_to_be_done": "Extract key insights about consumer behavior",
    "processing_timestamp": "2024-01-15T10:30:45.123456"
  },
  "extracted_sections": [
    {
      "document": "document1.pdf",
      "section_title": "Consumer Behavior Analysis",
      "importance_rank": 1,
      "page_number": 5
    }
  ],
  "subsection_analysis": [
    {
      "document": "document1.pdf",
      "refined_text": "Key insight about consumer preferences...",
      "page_number": 5
    }
  ]
}
```

## Docker Configuration

The Docker setup includes:
- Linux AMD64 platform compatibility
- Volume mounting for input/output
- Network isolation for security
- Automatic dependency installation
