import json
import re
from pathlib import Path

import numpy as np
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOCUMENT_DIR = PROJECT_ROOT / "data" / "multilingual"
QUERY_FILE = DOCUMENT_DIR / "queries.json"

MODEL_NAME = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"


def tokenize(text):
    return re.findall(r"\b\w+\b", text.lower())


def load_documents():
    documents = []

    for file_path in sorted(DOCUMENT_DIR.glob("m*.txt")):
        text = file_path.read_text(encoding="utf-8")
        documents.append({
            "id": file_path.stem,
            "text": text
        })

    return documents


def load_queries():
    with open(QUERY_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def normalize_scores(scores):
    minimum = np.min(scores)
    maximum = np.max(scores)

    if maximum == minimum:
        return np.zeros_like(scores)

    return (scores - minimum) / (maximum - minimum)


def cosine_similarity(query_embedding, document_embeddings):
    query_norm = np.linalg.norm(query_embedding)

    document_norms = np.linalg.norm(
        document_embeddings,
        axis=1
    )

    return np.dot(
        document_embeddings,
        query_embedding
    ) / (document_norms * query_norm)


def reciprocal_rank(ranked_indices, documents, relevant_docs, k=5):

    for rank, index in enumerate(ranked_indices[:k], start=1):

        document_id = documents[index]["id"]

        if document_id in relevant_docs:
            return 1 / rank

    return 0.0


def main():

    print("=" * 65)
    print("IndicSeek - Hybrid Alpha Tuning Experiment")
    print("=" * 65)

    documents = load_documents()
    queries = load_queries()

    print(f"\nDocuments: {len(documents)}")
    print(f"Queries: {len(queries)}")

    # -----------------------------
    # BM25
    # -----------------------------

    tokenized_documents = [
        tokenize(document["text"])
        for document in documents
    ]

    bm25 = BM25Okapi(tokenized_documents)

    # -----------------------------
    # Dense model
    # -----------------------------

    print("\nLoading multilingual model...")

    model = SentenceTransformer(MODEL_NAME)

    document_texts = [
        document["text"]
        for document in documents
    ]

    document_embeddings = model.encode(
        document_texts,
        convert_to_numpy=True,
        show_progress_bar=True
    )

    print(
        f"Embedding shape: {document_embeddings.shape}"
    )

    # -----------------------------
    # Alpha experiments
    # -----------------------------

    alphas = [0.0, 0.25, 0.50, 0.75, 1.0]

    results = []

    print("\n" + "=" * 65)
    print("ALPHA EXPERIMENT")
    print("=" * 65)

    for alpha in alphas:

        reciprocal_ranks = []

        for item in queries:

            query = item["query"]
            relevant_docs = item["relevant_docs"]

            # BM25
            query_tokens = tokenize(query)

            bm25_scores = bm25.get_scores(
                query_tokens
            )

            # Dense
            query_embedding = model.encode(
                query,
                convert_to_numpy=True
            )

            dense_scores = cosine_similarity(
                query_embedding,
                document_embeddings
            )

            # Normalize both scores
            normalized_bm25 = normalize_scores(
                bm25_scores
            )

            normalized_dense = normalize_scores(
                dense_scores
            )

            # Hybrid score
            hybrid_scores = (
                alpha * normalized_bm25
                +
                (1 - alpha) * normalized_dense
            )

            ranked_indices = np.argsort(
                hybrid_scores
            )[::-1]

            rr = reciprocal_rank(
                ranked_indices,
                documents,
                relevant_docs,
                k=5
            )

            reciprocal_ranks.append(rr)

        mrr = np.mean(reciprocal_ranks)

        results.append({
            "alpha": alpha,
            "bm25_weight": alpha,
            "dense_weight": 1 - alpha,
            "mrr@5": mrr
        })

        print(
            f"Alpha={alpha:.2f} | "
            f"BM25={alpha:.2f} | "
            f"Dense={1-alpha:.2f} | "
            f"MRR@5={mrr:.4f}"
        )

    # -----------------------------
    # Best configuration
    # -----------------------------

    best = max(
        results,
        key=lambda x: x["mrr@5"]
    )

    print("\n" + "=" * 65)
    print("BEST CONFIGURATION")
    print("=" * 65)

    print(
        f"Alpha:       {best['alpha']:.2f}"
    )

    print(
        f"BM25 weight: {best['bm25_weight']:.2f}"
    )

    print(
        f"Dense weight:{best['dense_weight']:.2f}"
    )

    print(
        f"MRR@5:       {best['mrr@5']:.4f}"
    )

    print("=" * 65)


if __name__ == "__main__":
    main()