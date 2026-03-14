
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def explain_gap(reg_clause, policy_clause, score):

    prompt = f"""
You are a banking compliance expert.

Regulatory Clause:
{reg_clause}

Policy Clause:
{policy_clause}

Similarity Score: {score}

Explain the compliance gap briefly.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content
