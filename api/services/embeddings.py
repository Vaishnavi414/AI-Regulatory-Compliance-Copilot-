"""
Embeddings Service - Generate semantic embeddings for text
Uses SentenceTransformers for creating vector representations
"""

from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Union
import logging

logger = logging.getLogger(__name__)

# Initialize the model globally for efficiency
_model = None


def get_model() -> SentenceTransformer:
    """
    Get or initialize the sentence transformer model.
    
    Returns:
        SentenceTransformer model instance
    """
    global _model
    if _model is None:
        logger.info("Loading SentenceTransformer model: all-MiniLM-L6-v2")
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def embed_texts(texts: Union[List[str], str]) -> np.ndarray:
    """
    Generate embeddings for a list of texts or a single text.
    
    Args:
        texts: List of text strings or a single text string
        
    Returns:
        Numpy array of embeddings
    """
    model = get_model()
    
    # Handle single string
    if isinstance(texts, str):
        texts = [texts]
    
    embeddings = model.encode(texts)
    return embeddings


def generate_embeddings(texts: List[str]) -> np.ndarray:
    """
    Generate embeddings for a list of texts.
    Alias for embed_texts for backward compatibility.
    
    Args:
        texts: List of text strings
        
    Returns:
        Numpy array of embeddings
    """
    return embed_texts(texts)


def get_embedding_dimension() -> int:
    """
    Get the dimension of embeddings produced by the model.
    
    Returns:
        Embedding dimension
    """
    model = get_model()
    return model.get_sentence_embedding_dimension()
