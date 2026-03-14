import faiss
import numpy as np


def build_index(embeddings):
    """
    Build a FAISS index from policy clause embeddings.
    
    Args:
        embeddings: numpy array of shape (n_clauses, embedding_dim)
    
    Returns:
        FAISS index object
    """
    # Get embedding dimension
    dimension = embeddings.shape[1]
    
    # Create L2 (Euclidean distance) index
    index = faiss.IndexFlatL2(dimension)
    
    # Add embeddings to index
    index.add(embeddings)
    
    return index


def search_similar(index, query_embeddings, k=1):
    """
    Search for most similar policy clauses for each regulatory clause.
    
    Args:
        index: FAISS index
        query_embeddings: numpy array of regulatory clause embeddings
        k: number of nearest neighbors to find (default: 1)
    
    Returns:
        distances: numpy array of L2 distances
        indices: numpy array of indices of most similar policy clauses
    """
    # Search for k nearest neighbors
    distances, indices = index.search(query_embeddings, k)
    
    return distances, indices
