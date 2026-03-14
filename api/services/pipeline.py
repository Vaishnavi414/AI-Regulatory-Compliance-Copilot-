"""
Pipeline Service - Orchestrates the full compliance analysis pipeline
Combines PDF parsing, chunking, embeddings, similarity, and classification
"""

import tempfile
from typing import Dict, List, Any, Optional
import logging
import io
import uuid
import datetime

from .pdf_parser import extract_text_from_bytes, extract_text_from_buffer
from .chunking import split_clauses, split_into_clauses
from .embeddings import embed_texts, generate_embeddings
from .similarity_engine import find_best_matches
from .classifier import classify_score, classify_compliance, calculate_risk, get_compliance_summary
from .rag_explainer import explain_gap, generate_summary
import os

logger = logging.getLogger(__name__)


async def run_analysis(
    regulation_file,
    policy_file,
    use_ai: bool = False,
    gemini_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Run full compliance analysis pipeline.
    
    Args:
        regulation_file: UploadFile for regulation PDF
        policy_file: UploadFile for policy PDF
        use_ai: Whether to generate AI explanations
        gemini_key: Optional Gemini API key
        
    Returns:
        Analysis results dictionary
    """
    # Save uploaded files to temporary files
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as reg_tmp:
        reg_tmp.write(await regulation_file.read())
        reg_path = reg_tmp.name

    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as pol_tmp:
        pol_tmp.write(await policy_file.read())
        pol_path = pol_tmp.name

    # Extract text from PDFs
    reg_text = extract_text(reg_path)
    pol_text = extract_text(pol_path)

    # Split into clauses
    reg_clauses = split_clauses(reg_text)
    pol_clauses = split_clauses(pol_text)

    # If no clauses found with primary method, try alternative
    if not reg_clauses:
        reg_clauses = split_into_clauses(reg_text)
    if not pol_clauses:
        pol_clauses = split_into_clauses(pol_text)

    logger.info(f"Found {len(reg_clauses)} regulatory clauses, {len(pol_clauses)} policy clauses")

    # Generate embeddings
    reg_embeddings = embed_texts(reg_clauses)
    pol_embeddings = embed_texts(pol_clauses)

    # Find best matches
    matches = find_best_matches(reg_embeddings, pol_embeddings, pol_clauses)

    # Process results
    results = []
    compliant_count = 0
    partial_count = 0
    missing_count = 0
    
    # Group matches by regulatory clause index
    match_idx = 0
    for i, reg_clause in enumerate(reg_clauses):
        if match_idx < len(matches):
            match = matches[match_idx]
            score = match["score"]
            policy_clause = match["policy_clause"]
            match_idx += 1
        else:
            score = 0.0
            policy_clause = ""

        # Classify compliance
        status = classify_score(score)
        
        # Get risk level
        _, risk = classify_compliance(score)

        # Count statuses
        if status == "Fully Compliant":
            compliant_count += 1
        elif status == "Partially Compliant":
            partial_count += 1
        else:
            missing_count += 1

        # Generate AI explanation if requested
        explanation = ""
        if use_ai and status != "Fully Compliant" and policy_clause:
            # Use provided key, or fall back to environment variable
            api_key = gemini_key or os.getenv("GEMINI_API_KEY")
            if api_key:
                from .rag_explainer import explain_with_gemini
                explanation = explain_with_gemini(
                    reg_clause, policy_clause, score, api_key
                )
            else:
                explanation = explain_gap(reg_clause, policy_clause, score)

        results.append({
            "id": str(uuid.uuid4()),
            "regulatory_clause": reg_clause[:300] + "..." if len(reg_clause) > 300 else reg_clause,
            "full_regulatory_clause": reg_clause,
            "matched_policy_clause": policy_clause[:300] + "..." if len(policy_clause) > 300 else policy_clause,
            "full_policy_clause": policy_clause,
            "similarity_score": float(score),
            "status": status,
            "risk": risk,
            "explanation": explanation
        })

    # Calculate risk score
    risk_score = calculate_risk(compliant_count, partial_count, missing_count)
    
    # Generate summary
    summary = generate_summary(compliant_count, partial_count, missing_count, len(results))

    return {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.datetime.now().isoformat(),
        "total_clauses": len(results),
        "compliant": compliant_count,
        "partial": partial_count,
        "missing": missing_count,
        "risk_score": risk_score,
        "results": results,
        "summary": summary
    }


def run_analysis_sync(
    reg_bytes: bytes,
    pol_bytes: bytes,
    use_ai: bool = False,
    gemini_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Synchronous version of run_analysis for non-async contexts.
    
    Args:
        reg_bytes: Regulation PDF as bytes
        pol_bytes: Policy PDF as bytes
        use_ai: Whether to generate AI explanations
        gemini_key: Optional Gemini API key
        
    Returns:
        Analysis results dictionary
    """
    # Create BytesIO buffers
    reg_buffer = io.BytesIO(reg_bytes)
    pol_buffer = io.BytesIO(pol_bytes)
    
    # Extract text
    reg_text = extract_text_from_buffer(reg_buffer)
    pol_text = extract_text_from_buffer(pol_buffer)
    
    # Split into clauses
    reg_clauses = split_clauses(reg_text)
    pol_clauses = split_clauses(pol_text)
    
    if not reg_clauses:
        reg_clauses = split_into_clauses(reg_text)
    if not pol_clauses:
        pol_clauses = split_into_clauses(pol_text)
    
    # Generate embeddings
    reg_embeddings = embed_texts(reg_clauses)
    pol_embeddings = embed_texts(pol_clauses)
    
    # Find matches
    matches = find_best_matches(reg_embeddings, pol_embeddings, pol_clauses)
    
    # Process results
    results = []
    compliant_count = 0
    partial_count = 0
    missing_count = 0
    
    for i, reg_clause in enumerate(reg_clauses):
        if i < len(matches):
            match = matches[i]
            score = match["score"]
            policy_clause = match["policy_clause"]
        else:
            score = 0.0
            policy_clause = ""
        
        status = classify_score(score)
        _, risk = classify_compliance(score)
        
        if status == "Fully Compliant":
            compliant_count += 1
        elif status == "Partially Compliant":
            partial_count += 1
        else:
            missing_count += 1
        
        explanation = ""
        if use_ai and status != "Fully Compliant" and policy_clause:
            if gemini_key:
                from .rag_explainer import explain_with_gemini
                explanation = explain_with_gemini(reg_clause, policy_clause, score, gemini_key)
            else:
                explanation = explain_gap(reg_clause, policy_clause, score)
        
        results.append({
            "regulatory_clause": reg_clause[:300] + "..." if len(reg_clause) > 300 else reg_clause,
            "matched_policy_clause": policy_clause[:300] + "..." if len(policy_clause) > 300 else policy_clause,
            "similarity_score": float(score),
            "status": status,
            "risk": risk,
            "explanation": explanation
        })
    
    risk_score = calculate_risk(compliant_count, partial_count, missing_count)
    
    return {
        "total_clauses": len(results),
        "compliant": compliant_count,
        "partial": partial_count,
        "missing": missing_count,
        "risk_score": risk_score,
        "results": results
    }
