"""
Similarity Engine Service - Find similar text using embeddings
Supports both FAISS and sklearn cosine similarity
"""

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


def find_best_matches(
    reg_embeddings: np.ndarray, 
    pol_embeddings: np.ndarray, 
    pol_clauses: List[str],
    top_k: int = 1
) -> List[Dict[str, Any]]:
    """
    Find the best matching policy clauses for each regulatory clause.
    
    Args:
        reg_embeddings: Embeddings for regulatory clauses
        pol_embeddings: Embeddings for policy clauses
        pol_clauses: List of policy clause texts
        top_k: Number of top matches to return
        
    Returns:
        List of matches with policy clause and score
    """
    # Calculate cosine similarity between all pairs
    sims = cosine_similarity(reg_embeddings, pol_embeddings)
    
    matches = []
    
    for row in sims:
        # Get top-k indices
        top_indices = row.argsort()[-top_k:][::-1]
        
        for idx in top_indices:
            matches.append({
                "policy_clause": pol_clauses[idx],
                "score": float(row[idx]),
                "index": int(idx)
            })
        
        # If only top 1, just add the best match
        if top_k == 1:
            matches[-1]["rank"] = 1
    
    return matches


def compute_similarity_matrix(
    source_embeddings: np.ndarray, 
    target_embeddings: np.ndarray
) -> np.ndarray:
    """
    Compute similarity matrix between source and target embeddings.
    
    Args:
        source_embeddings: Embeddings for source texts
        target_embeddings: Embeddings for target texts
        
    Returns:
        Similarity matrix
    """
    return cosine_similarity(source_embeddings, target_embeddings)


def get_top_matches(
    similarities: np.ndarray, 
    top_k: int = 5
) -> List[tuple]:
    """
    Get top-k matches from similarity matrix.
    
    Args:
        similarities: Similarity matrix
        top_k: Number of top matches
        
    Returns:
        List of (source_idx, target_idx, score) tuples
    """
    matches = []
    for i in range(similarities.shape[0]):
        row = similarities[i]
        top_indices = row.argsort()[-top_k:][::-1]
        for j in top_indices:
            matches.append((i, j, row[j]))
    return matches


def convert_distance_to_similarity(distance: float) -> float:
    """
    Convert distance to similarity score.
    
    Args:
        distance: Distance value (e.g., from FAISS)
        
    Returns:
        Similarity score between 0 and 1
    """
    return 1 / (1 + distance)
