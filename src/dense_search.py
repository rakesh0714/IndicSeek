import json
import re
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOCUMENT_DIR = PROJECT_ROOT / "data" / "documents"
QUERY_FILE = PROJECT_ROOT / "data" / "queries" / "queries.json"


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def load_documents():
    documents = []

    for file_path in sorted(DOCUMENT_DIR.glob("*.txt")):
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

    similarities = np.dot(
        document_embeddings,
        query_embedding
    ) / (document_norms * query_norm)

    return similarities


def search(model, documents, document_embeddings, query, top_k=5):

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
            "score": float(scores[index]),
            "text": documents[index]["text"]
        })

    return results


def reciprocal_rank(results, relevant_documents):

    for rank, result in enumerate(results, start=1):

        if result["document_id"] in relevant_documents:
            return 1 / rank

    return 0.0


def recall_at_k(results, relevant_documents):

    retrieved = {
        result["document_id"]
        for result in results
    }

    relevant = set(relevant_documents)

    if not relevant:
        return 0.0

    return len(retrieved & relevant) / len(relevant)


def main():

    print("=" * 60)
    print("IndicSeek - Dense Retrieval")
    print("=" * 60)

    print("\nLoading documents...")

    documents = load_documents()

    print(f"Documents loaded: {len(documents)}")

    print("\nLoading embedding model...")

    model = SentenceTransformer(MODEL_NAME)

    print(f"Model: {MODEL_NAME}")

    print("\nCreating document embeddings...")

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
    recalls = []

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

        recall = recall_at_k(
            results,
            relevant_docs
        )

        reciprocal_ranks.append(rr)
        recalls.append(recall)

        print("\n" + "-" * 60)

        print(f"Query: {query}")

        print(
            f"Relevant documents: {relevant_docs}"
        )

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

    mean_recall = sum(recalls) / len(
        recalls
    )

    print("\n" + "=" * 60)
    print("FINAL DENSE RETRIEVAL RESULTS")
    print("=" * 60)

    print(f"MRR@5:    {mrr:.4f}")
    print(f"Recall@5: {mean_recall:.4f}")

    print("=" * 60)


if __name__ == "__main__":
    main()