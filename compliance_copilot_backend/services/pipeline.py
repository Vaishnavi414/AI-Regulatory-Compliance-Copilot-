
import tempfile
from services.pdf_parser import extract_text
from services.chunking import split_clauses
from services.embeddings import embed_texts
from services.similarity_engine import find_best_matches
from services.classifier import classify_score
from services.rag_explainer import explain_gap

async def run_analysis(regulation_file, policy_file):

    with tempfile.NamedTemporaryFile(delete=False) as reg_tmp:
        reg_tmp.write(await regulation_file.read())
        reg_path = reg_tmp.name

    with tempfile.NamedTemporaryFile(delete=False) as pol_tmp:
        pol_tmp.write(await policy_file.read())
        pol_path = pol_tmp.name

    reg_text = extract_text(reg_path)
    pol_text = extract_text(pol_path)

    reg_clauses = split_clauses(reg_text)
    pol_clauses = split_clauses(pol_text)

    reg_embeddings = embed_texts(reg_clauses)
    pol_embeddings = embed_texts(pol_clauses)

    matches = find_best_matches(reg_embeddings, pol_embeddings, pol_clauses)

    results = []

    for i, match in enumerate(matches):

        score = match["score"]
        policy_clause = match["policy_clause"]

        status = classify_score(score)

        explanation = explain_gap(
            reg_clauses[i],
            policy_clause,
            score
        )

        results.append({
            "regulatory_clause": reg_clauses[i],
            "matched_policy_clause": policy_clause,
            "similarity_score": float(score),
            "status": status,
            "explanation": explanation
        })

    return {"results": results}
