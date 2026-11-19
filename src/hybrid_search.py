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


def reciprocal_rank(results, relevant_docs):
    for rank, result in enumerate(results, start=1):
        if result["document_id"] in relevant_docs:
            return 1 / rank

    return 0.0


def main():

    print("=" * 60)
    print("IndicSeek - Hybrid Retrieval")
    print("=" * 60)

    documents = load_documents()

    print(f"\nDocuments loaded: {len(documents)}")

    queries = load_queries()

    print(f"Evaluation queries: {len(queries)}")

    # ---------------------------------------------------------
    # BM25
    # ---------------------------------------------------------

    tokenized_documents = [
        tokenize(document["text"])
        for document in documents
    ]

    bm25 = BM25Okapi(tokenized_documents)

    # ---------------------------------------------------------
    # Multilingual Dense Model
    # ---------------------------------------------------------

    print("\nLoading multilingual embedding model...")

    model = SentenceTransformer(MODEL_NAME)

    document_texts = [
        document["text"]
        for document in documents
    ]

    print("Creating document embeddings...")

    document_embeddings = model.encode(
        document_texts,
        convert_to_numpy=True,
        show_progress_bar=True
    )

    print(
        f"Embedding shape: {document_embeddings.shape}"
    )

    # ---------------------------------------------------------
    # Hybrid weights
    # ---------------------------------------------------------

    alpha = 0.5

    print(f"\nHybrid weight alpha: {alpha}")
    print("BM25 weight: 0.5")
    print("Dense weight: 0.5")

    reciprocal_ranks = []

    # ---------------------------------------------------------
    # Search
    # ---------------------------------------------------------

    for item in queries:

        query = item["query"]
        relevant_docs = item["relevant_docs"]

        # BM25 scores
        query_tokens = tokenize(query)

        bm25_scores = bm25.get_scores(
            query_tokens
        )

        # Dense scores
        query_embedding = model.encode(
            query,
            convert_to_numpy=True
        )

        dense_scores = cosine_similarity(
            query_embedding,
            document_embeddings
        )

        # Normalize both scoring systems
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
        )[::-1][:5]

        results = []

        for index in ranked_indices:

            results.append({
                "document_id": documents[index]["id"],
                "bm25_score": float(
                    normalized_bm25[index]
                ),
                "dense_score": float(
                    normalized_dense[index]
                ),
                "hybrid_score": float(
                    hybrid_scores[index]
                )
            })

        rr = reciprocal_rank(
            results,
            relevant_docs
        )

        reciprocal_ranks.append(rr)

        print("\n" + "-" * 60)

        print(f"Query: {query}")
        print(f"Relevant: {relevant_docs}")
        print(f"Reciprocal Rank: {rr:.4f}")

        print("\nTop results:")

        for rank, result in enumerate(
            results,
            start=1
        ):

            marker = (
                "✓"
                if result["document_id"] in relevant_docs
                else ""
            )

            print(
                f"{rank}. "
                f"{result['document_id']} "
                f"Hybrid={result['hybrid_score']:.4f} "
                f"BM25={result['bm25_score']:.4f} "
                f"Dense={result['dense_score']:.4f} "
                f"{marker}"
            )

    # ---------------------------------------------------------
    # Final result
    # ---------------------------------------------------------

    mrr = sum(reciprocal_ranks) / len(
        reciprocal_ranks
    )

    print("\n" + "=" * 60)
    print("FINAL HYBRID RESULTS")
    print("=" * 60)

    print(f"MRR@5: {mrr:.4f}")

    print("=" * 60)


if __name__ == "__main__":
    main()