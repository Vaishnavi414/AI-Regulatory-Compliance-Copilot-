"""
RAG Explainer Service - AI-powered explanations for compliance gaps
Uses OpenAI GPT models or Google Gemini for generating explanations
"""

import os
from typing import Optional
import logging
from pathlib import Path

# Load environment variables from .env file
from dotenv import load_dotenv

# Get the directory of this file (api/services/)
_services_dir = Path(__file__).parent
# Go up to api/ directory
_api_dir = _services_dir.parent
# Look for .env in api/ directory
_env_file = _api_dir / ".env"

# Try to load .env file if it exists
if _env_file.exists():
    load_dotenv(_env_file)
else:
    # Also try loading from current working directory
    load_dotenv()

logger = logging.getLogger(__name__)

# OpenAI client (lazy initialization)
_openai_client = None


def get_openai_client():
    """
    Get or initialize OpenAI client.
    
    Returns:
        OpenAI client instance
    """
    global _openai_client
    if _openai_client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            from openai import OpenAI
            _openai_client = OpenAI(api_key=api_key)
        else:
            logger.warning("OPENAI_API_KEY not found in environment")
    return _openai_client


def explain_gap(
    reg_clause: str, 
    policy_clause: str, 
    score: float,
    model: str = "gpt-4o-mini"
) -> str:
    """
    Generate AI explanation for a compliance gap using OpenAI.
    
    Args:
        reg_clause: The regulatory clause text
        policy_clause: The matched policy clause text
        score: Similarity score
        model: OpenAI model to use
        
    Returns:
        AI-generated explanation
    """
    client = get_openai_client()
    
    if not client:
        return "AI explanation unavailable - OpenAI API key not configured"
    
    prompt = f"""
You are a banking compliance expert. Analyze the following regulatory clause and policy clause to explain the compliance gap.

Regulatory Clause:
{reg_clause[:500]}

Policy Clause:
{policy_clause[:500]}

Similarity Score: {score:.2f}

Provide a brief explanation (2-3 sentences) of:
1. What the regulatory requirement mandates
2. How the policy addresses (or fails to address) it
3. Recommended action if non-compliant

Focus on actionable compliance insights.
"""
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error generating explanation: {e}")
        return f"AI explanation generation failed: {str(e)}"


def explain_with_gemini(
    reg_clause: str,
    policy_clause: str,
    score: float,
    gemini_key: str = None
) -> str:
    """
    Generate explanation using Google Gemini API.
    
    Args:
        reg_clause: The regulatory clause text
        policy_clause: The matched policy clause text  
        score: Similarity score
        gemini_key: Google Gemini API key (optional, will use env var if not provided)
        
    Returns:
        AI-generated explanation
    """
    # Use provided key or get from environment
    api_key = gemini_key or os.getenv("REMOVED")
    
    if not api_key:
        return "AI explanation unavailable - GEMINI_API_KEY not configured"
    
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        
        model = genai.GenerativeModel('gemini-pro')
        
        prompt = f"""
As a compliance expert, explain the gap between:

Regulatory Requirement: {reg_clause[:500]}

Current Policy: {policy_clause[:500]}

Similarity: {score:.2f}

Provide a concise explanation of the compliance status and recommended actions.
"""
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        logger.error(f"Error with Gemini explanation: {e}")
        # Fallback to OpenAI if available
        return explain_gap(reg_clause, policy_clause, score)


def generate_summary(
    compliant_count: int,
    partial_count: int,
    missing_count: int,
    total: int
) -> str:
    """
    Generate overall compliance summary.
    
    Args:
        compliant_count: Number of fully compliant clauses
        partial_count: Number of partially compliant clauses
        missing_count: Number of missing clauses
        total: Total number of clauses
        
    Returns:
        Summary text
    """
    compliant_pct = (compliant_count / total * 100) if total > 0 else 0
    missing_pct = (missing_count / total * 100) if total > 0 else 0
    
    if missing_pct > 30:
        status = "HIGH RISK - Significant compliance gaps identified"
    elif missing_pct > 15:
        status = "MEDIUM RISK - Some compliance improvements needed"
    else:
        status = "LOW RISK - Generally compliant"
    
    return f"""
Compliance Analysis Summary:
- Total Clauses Analyzed: {total}
- Fully Compliant: {compliant_count} ({compliant_pct:.1f}%)
- Partially Compliant: {partial_count}
- Not Addressed: {missing_count} ({missing_pct:.1f}%)

Overall Status: {status}
"""


def check_api_configuration() -> dict:
    """
    Check which AI APIs are configured.
    
    Returns:
        Dictionary with configuration status
    """
    return {
        "openai_configured": bool(os.getenv("OPENAI_API_KEY")),
        "gemini_configured": bool(os.getenv("GEMINI_API_KEY"))
    }
