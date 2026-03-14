
# AI Regulatory Compliance Copilot (Backend)

Prototype backend for automated policy-to-regulation gap analysis.

## Features
- Upload regulatory + policy PDFs
- Clause chunking
- Semantic similarity comparison
- Compliance classification
- AI explanation generation

## Run

Install dependencies:

pip install -r requirements.txt

Start server:

uvicorn main:app --reload

API:

POST /analyze
Upload:
- regulation PDF
- policy PDF
