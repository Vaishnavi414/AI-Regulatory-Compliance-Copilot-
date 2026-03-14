# AI Regulatory Compliance Copilot

A lightweight, laptop-friendly system that compares regulatory documents with internal policy documents to identify compliance gaps using semantic similarity.

## 🚀 Features

- **PDF Text Extraction**: Uses PyMuPDF to extract text from regulatory and policy PDFs
- **Semantic Matching**: Uses SentenceTransformers (all-MiniLM-L6-v2) for efficient CPU-based embeddings
- **Vector Search**: FAISS for fast similarity search
- **Compliance Classification**: 
  - 🟢 Fully Compliant (> 0.85 similarity)
  - 🟡 Partially Compliant (0.65 - 0.85 similarity)
  - 🔴 Not Addressed (< 0.65 similarity)
- **Risk Scoring**: Weighted risk assessment based on compliance gaps
- **AI Explanations**: Optional Gemini API integration for detailed gap analysis

## 📋 Requirements

- Python 3.8+
- 8GB RAM (laptop-friendly)
- No GPU required

## 🛠️ Installation

1. **Clone the repository** and navigate to the project directory:

```bash
cd AI-Regulatory-Compliance-Copilot
```

2. **Create a virtual environment** (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:

```bash
pip install -r requirements.txt
```

## ⚡ Usage

1. **Run the Streamlit application**:

```bash
streamlit run app.py
```

2. **Open your browser** to `http://localhost:8501`

3. **Upload documents**:
   - Upload a Regulatory Document PDF
   - Upload an Internal Policy Document PDF

4. **Click "Analyze Compliance"** to see results

5. **(Optional) Enable Gemini explanations**:
   - Check "Use Gemini for explanations" in the sidebar
   - Enter your Gemini API key

## 📁 Project Structure

```
AI-Regulatory-Compliance-Copilot/
├── app.py                 # Main Streamlit application
├── preprocessing.py       # PDF text extraction and clause splitting
├── embeddings.py         # SentenceTransformer embeddings
├── similarity.py        # FAISS index and search
├── classifier.py        # Compliance classification and risk scoring
├── rag_generator.py     # Gemini API integration
├── requirements.txt     # Python dependencies
├── README.md            # This file
└── data/                # Sample PDFs (optional)
    ├── regulatory_sample.pdf
    └── policy_sample.pdf
```

## 🔧 Configuration

### Compliance Thresholds

You can modify thresholds in `classifier.py`:

```python
# Current thresholds
if score > 0.85:
    return "Fully Compliant"
elif score > 0.65:
    return "Partially Compliant"
else:
    return "Not Addressed"
```

### Risk Scoring

Risk points are calculated in `classifier.py`:

- Not Addressed: 2 points
- Partially Compliant: 1 point
- Fully Compliant: 0 points

## 📝 Sample Documents

Place sample PDFs in the `data/` folder for testing:

- `regulatory_sample.pdf` - Example regulatory requirements
- `policy_sample.pdf` - Example internal policy document

## 🔐 API Keys

### Gemini API (Optional)

To enable AI-generated explanations:

1. Get a Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Enter it in the sidebar when running the app

## 🧪 Testing

Run a quick test:

```bash
# Check if all imports work
python -c "
from preprocessing import extract_text, split_into_clauses
from embeddings import generate_embeddings
from similarity import build_index, search_similar
from classifier import classify_compliance, calculate_risk
print('All imports successful!')
"
```

## 📊 How It Works

1. **Text Extraction**: PyMuPDF reads text from both PDFs
2. **Clause Splitting**: Documents are split into meaningful paragraphs/clauses
3. **Embedding Generation**: Each clause is converted to a 384-dimensional vector
4. **Index Building**: Policy clause embeddings are stored in FAISS
5. **Similarity Search**: For each regulatory clause, find the most similar policy clause
6. **Classification**: Score determines compliance status
7. **Risk Calculation**: Aggregate risk based on gaps

## ⚠️ Limitations

- Semantic similarity is not perfect - always review results manually
- Gemini API requires internet connection and API key
- Large PDFs may take longer to process
- Works best with clearly formatted documents

## 📄 License

MIT License - Feel free to use for your hackathon projects!

## 🙏 Acknowledgments

- [SentenceTransformers](https://sbert.net/) for the embedding model
- [FAISS](https://faiss.ai/) for efficient similarity search
- [Streamlit](https://streamlit.io/) for the UI
- [PyMuPDF](https://pymupdf.readthedocs.io/) for PDF processing
