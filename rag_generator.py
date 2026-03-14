import os
import google.generativeai as genai


def configure_gemini(api_key=None):
    """
    Configure Gemini API with the provided key.
    Falls back to environment variable if no key provided.
    """
    if api_key:
        genai.configure(api_key=api_key)
    elif os.environ.get("GEMINI_API_KEY"):
        genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
    else:
        raise ValueError("Gemini API key not provided")


def generate_explanation(reg_clause, policy_clause):
    """
    Generate a compliance gap explanation using Gemini API.
    
    Args:
        reg_clause: The regulatory requirement clause
        policy_clause: The matched policy clause
    
    Returns:
        Explanation text or error message
    """
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        prompt = f"""
You are a compliance expert. Compare the following regulatory clause and policy clause 
and explain any compliance gaps in 2-3 short bullet points.

Regulatory Clause:
{reg_clause[:500]}

Policy Clause:
{policy_clause[:500]}

Focus on:
1. What the regulation requires
2. What the policy currently states
3. The specific gap or missing requirement

Keep your response concise and actionable.
"""
        
        response = model.generate_content(prompt)
        
        return response.text
        
    except Exception as e:
        return f"Could not generate explanation: {str(e)}"
