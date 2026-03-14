from sentence_transformers import SentenceTransformer


# Load model once (lightweight)
model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embeddings(clauses):
    """
    Convert clauses into vector embeddings.
    """

    embeddings = model.encode(
        clauses,
        convert_to_numpy=True,
        show_progress_bar=False
    )

    return embeddings