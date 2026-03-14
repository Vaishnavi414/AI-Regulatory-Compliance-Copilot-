"""
Classifier Service - Classify compliance status based on similarity scores
"""

from typing import Dict, Tuple


def classify_score(score: float) -> str:
    """
    Classify compliance status based on similarity score.
    
    Args:
        score: Similarity score between 0 and 1
        
    Returns:
        Compliance status string
    """
    if score > 0.85:
        return "Fully Compliant"
    elif score > 0.60:
        return "Partially Compliant"
    else:
        return "Not Addressed"


def classify_compliance(
    similarity_score: float, 
    threshold: float = 0.75
) -> Tuple[str, str]:
    """
    Classify compliance status with configurable threshold.
    
    Args:
        similarity_score: Similarity score between 0 and 1
        threshold: Minimum score for compliance
        
    Returns:
        Tuple of (status, risk_level)
    """
    if similarity_score > threshold:
        status = "Compliant"
        risk = "Low"
    elif similarity_score > (threshold - 0.2):
        status = "Partial"
        risk = "Medium"
    else:
        status = "Missing"
        risk = "High"
    
    return status, risk


def calculate_risk(
    compliant: int, 
    partial: int, 
    missing: int
) -> int:
    """
    Calculate overall risk score based on compliance counts.
    
    Args:
        compliant: Number of compliant clauses
        partial: Number of partially compliant clauses
        missing: Number of missing clauses
        
    Returns:
        Risk score (higher = more risky)
    """
    return missing * 2 + partial * 1


def get_compliance_summary(
    results: list
) -> Dict[str, int]:
    """
    Get compliance summary from analysis results.
    
    Args:
        results: List of analysis results
        
    Returns:
        Dictionary with counts of each status
    """
    summary = {
        "compliant": 0,
        "partial": 0,
        "missing": 0,
        "total": len(results)
    }
    
    for result in results:
        status = result.get("status", "").lower()
        if "compliant" in status and "partial" not in status:
            summary["compliant"] += 1
        elif "partial" in status:
            summary["partial"] += 1
        else:
            summary["missing"] += 1
    
    return summary
