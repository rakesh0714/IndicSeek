import json
import re
from pathlib import Path

import numpy as np
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOCUMENT_DIR = PROJECT_ROOT / "data" / "dev_documents"

MODEL_NAME = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"

TOP_K = 5
ALPHA = 0.50


def tokenize(text):
    return re.findall(r"\b\w+\b", text.lower())


def load_documents():
    documents = []

    for file_path in sorted(DOCUMENT_DIR.glob("d*.txt")):
        documents.append({
            "id": file_path.stem,
            "text": file_path.read_text(encoding="utf-8")
        })

    return documents


def normalize(scores):
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


def main():

    print("=" * 70)
    print("IndicSeek - Retrieval Pipeline")
    print("=" * 70)

    documents = load_documents()

    print(f"\nDocuments loaded: {len(documents)}")

    # --------------------------------------------------
    # BM25
    # --------------------------------------------------

    print("\nBuilding BM25 index...")

    tokenized_documents = [
        tokenize(document["text"])
        for document in documents
    ]

    bm25 = BM25Okapi(tokenized_documents)

    # --------------------------------------------------
    # Dense Model
    # --------------------------------------------------

    print("\nLoading multilingual dense model...")

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

    # --------------------------------------------------
    # User Query
    # --------------------------------------------------

    print("\n" + "=" * 70)

    query = input(
        "\nEnter your query: "
    ).strip()

    if not query:
        print("Query cannot be empty.")
        return

    # --------------------------------------------------
    # BM25 Scores
    # --------------------------------------------------

    query_tokens = tokenize(query)

    bm25_scores = bm25.get_scores(
        query_tokens
    )

    # --------------------------------------------------
    # Dense Scores
    # --------------------------------------------------

    query_embedding = model.encode(
        query,
        convert_to_numpy=True
    )

    dense_scores = cosine_similarity(
        query_embedding,
        document_embeddings
    )

    # --------------------------------------------------
    # Hybrid Scores
    # --------------------------------------------------

    bm25_normalized = normalize(
        bm25_scores
    )

    dense_normalized = normalize(
        dense_scores
    )

    hybrid_scores = (
        ALPHA * bm25_normalized
        + (1 - ALPHA) * dense_normalized
    )

    ranked_indices = np.argsort(
        hybrid_scores
    )[::-1]

    # --------------------------------------------------
    # Display Results
    # --------------------------------------------------

    print("\n" + "=" * 70)
    print("RETRIEVED EVIDENCE")
    print("=" * 70)

    print(
        f"\nQuery: {query}"
    )

    print(
        f"\nTop {TOP_K} documents "
        f"(Hybrid alpha={ALPHA})"
    )

    print("-" * 70)

    for rank, index in enumerate(
        ranked_indices[:TOP_K],
        start=1
    ):

        document = documents[index]

        print(
            f"\nRank {rank}"
        )

        print(
            f"Document ID : {document['id']}"
        )

        print(
            f"BM25 Score  : {bm25_scores[index]:.4f}"
        )

        print(
            f"Dense Score : {dense_scores[index]:.4f}"
        )

        print(
            f"Hybrid Score: {hybrid_scores[index]:.4f}"
        )

        print(
            "\nEvidence:"
        )

        print(
            document["text"][:700]
        )

        print("-" * 70)


if __name__ == "__main__":
    main()