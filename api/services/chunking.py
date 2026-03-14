"""
Chunking Service - Split documents into clauses/sections
"""

import re
from typing import List


def split_clauses(text: str, min_length: int = 100) -> List[str]:
    """
    Split text into clauses using numbered patterns.
    
    Args:
        text: Input text to split
        min_length: Minimum length of clause to include
        
    Returns:
        List of text clauses
    """
    # Split by numbered patterns like "1.", "2.", etc.
    clauses = re.split(r'\n\d+\.', text)
    # Filter out short clauses
    return [c.strip() for c in clauses if len(c.strip()) > min_length]


def split_into_clauses(text: str, min_length: int = 50) -> List[str]:
    """
    Alternative clause splitting with more patterns.
    Uses multiple strategies to split text into meaningful chunks.
    
    Args:
        text: Input text to split
        min_length: Minimum length of clause to include
        
    Returns:
        List of text clauses
    """
    # Try multiple splitting strategies
    
    # Strategy 1: Numbered sections
    clauses = re.split(r'(?:\n|^)(\d+\.)\s+', text)
    if len(clauses) > 2:
        # Reconstruct numbered sections
        result = []
        for i in range(1, len(clauses), 2):
            if i+1 < len(clauses):
                section_num = clauses[i]
                section_text = clauses[i+1]
                result.append(f"{section_num} {section_text}")
            elif clauses[i]:
                result.append(clauses[i])
        if result:
            return [c.strip() for c in result if len(c.strip()) > min_length]
    
    # Strategy 2: Paragraphs with significant content
    paragraphs = text.split('\n\n')
    result = [p.strip() for p in paragraphs if len(p.strip()) > min_length]
    
    if not result:
        # Strategy 3: Split by sentences if nothing else works
        sentences = re.split(r'(?<=[.!?])\s+', text)
        result = [s.strip() for s in sentences if len(s.strip()) > min_length]
    
    return result


def chunk_by_sentences(text: str, chunk_size: int = 5) -> List[str]:
    """
    Split text into chunks of sentences.
    
    Args:
        text: Input text
        chunk_size: Number of sentences per chunk
        
    Returns:
        List of text chunks
    """
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    
    for i in range(0, len(sentences), chunk_size):
        chunk = ' '.join(sentences[i:i+chunk_size])
        if chunk.strip():
            chunks.append(chunk.strip())
    
    return chunks
