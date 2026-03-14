"""
PDF Parser Service - Extract text from PDF documents
Uses PyMuDF (fitz) for PDF text extraction
"""

import fitz
import io


def extract_text(file_path: str) -> str:
    """
    Extract text from a PDF file.
    
    Args:
        file_path: Path to the PDF file
        
    Returns:
        Extracted text as string
    """
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def extract_text_from_bytes(file_bytes: bytes) -> str:
    """
    Extract text from PDF bytes.
    
    Args:
        file_bytes: PDF file as bytes
        
    Returns:
        Extracted text as string
    """
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def extract_text_from_buffer(buffer: io.BytesIO) -> str:
    """
    Extract text from a BytesIO buffer.
    
    Args:
        buffer: BytesIO buffer containing PDF
        
    Returns:
        Extracted text as string
    """
    doc = fitz.open(stream=buffer.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text
