import fitz
import re
import io


def extract_text(pdf_file):
    """
    Extract text from PDF using PyMuPDF.
    Works with Streamlit uploaded files, BytesIO, or file paths.
    """
    text = ""

    # Handle different input types
    if isinstance(pdf_file, io.BytesIO):
        # BytesIO object
        with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()
    elif hasattr(pdf_file, 'read'):
        # Streamlit uploaded file or file-like object
        with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()
    else:
        # File path
        with fitz.open(pdf_file) as doc:
            for page in doc:
                text += page.get_text()

    return text


def split_into_clauses(text):
    """
    Split document text into clauses or paragraphs.
    Removes very small fragments to keep meaningful chunks.
    """

    # split by paragraph breaks
    clauses = re.split(r'\n\s*\n', text)

    cleaned_clauses = []

    for clause in clauses:
        clause = clause.strip()

        # keep only meaningful clauses
        if len(clause) > 40:
            cleaned_clauses.append(clause)

    return cleaned_clauses
