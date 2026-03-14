
from sklearn.metrics.pairwise import cosine_similarity

def find_best_matches(reg_embeddings, pol_embeddings, pol_clauses):

    sims = cosine_similarity(reg_embeddings, pol_embeddings)

    matches = []

    for row in sims:
        idx = row.argmax()
        matches.append({
            "policy_clause": pol_clauses[idx],
            "score": row[idx]
        })

    return matches
