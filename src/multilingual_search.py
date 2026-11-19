import json
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOCUMENT_DIR = PROJECT_ROOT / "data" / "multilingual"
QUERY_FILE = DOCUMENT_DIR / "queries.json"

MODEL_NAME = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"


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


def search(
    model,
    documents,
    document_embeddings,
    query,
    top_k=5
):
    query_embedding = model.encode(
        query,
        convert_to_numpy=True
    )

    scores = cosine_similarity(
        query_embedding,
        document_embeddings
    )

    ranked_indices = np.argsort(scores)[::-1][:top_k]

    results = []

    for index in ranked_indices:
        results.append({
            "document_id": documents[index]["id"],
            "score": float(scores[index])
        })

    return results


def reciprocal_rank(results, relevant_docs):
    for rank, result in enumerate(results, start=1):
        if result["document_id"] in relevant_docs:
            return 1 / rank

    return 0.0


def main():

    print("=" * 60)
    print("IndicSeek - Multilingual Dense Retrieval")
    print("=" * 60)

    documents = load_documents()

    print(f"\nDocuments loaded: {len(documents)}")

    print("\nLoading embedding model...")

    model = SentenceTransformer(MODEL_NAME)

    print(f"Model: {MODEL_NAME}")

    print("\nCreating multilingual document embeddings...")

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

    queries = load_queries()

    print(f"Evaluation queries: {len(queries)}")

    reciprocal_ranks = []

    for item in queries:

        query = item["query"]
        relevant_docs = item["relevant_docs"]

        results = search(
            model,
            documents,
            document_embeddings,
            query,
            top_k=5
        )

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
                f"Score={result['score']:.4f} "
                f"{marker}"
            )

    mrr = sum(reciprocal_ranks) / len(
        reciprocal_ranks
    )

    print("\n" + "=" * 60)
    print("FINAL MULTILINGUAL RESULTS")
    print("=" * 60)

    print(f"MRR@5: {mrr:.4f}")

    print("=" * 60)


if __name__ == "__main__":
    main()