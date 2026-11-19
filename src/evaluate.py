import json
import re
from pathlib import Path

from rank_bm25 import BM25Okapi

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOCUMENT_DIR = PROJECT_ROOT / "data" / "documents"
QUERY_FILE = PROJECT_ROOT / "data" / "queries" / "queries.json"


def tokenize(text):
    text = text.lower()
    return re.findall(r"\b\w+\b", text)


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


def search(bm25, documents, query, top_k=5):
    query_tokens = tokenize(query)

    scores = bm25.get_scores(query_tokens)

    ranked_indices = scores.argsort()[::-1][:top_k]

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


def recall_at_k(results, relevant_docs):
    retrieved_docs = {
        result["document_id"]
        for result in results
    }

    relevant_docs = set(relevant_docs)

    if not relevant_docs:
        return 0.0

    return len(retrieved_docs & relevant_docs) / len(relevant_docs)


def dcg_at_k(results, relevant_docs, k=5):
    dcg = 0.0

    for rank, result in enumerate(results[:k], start=1):

        if result["document_id"] in relevant_docs:
            relevance = 1
        else:
            relevance = 0

        dcg += relevance / __import__("math").log2(rank + 1)

    return dcg


def ndcg_at_k(results, relevant_docs, k=5):
    actual_dcg = dcg_at_k(results, relevant_docs, k)

    ideal_results = [
        {"document_id": doc_id}
        for doc_id in relevant_docs
    ]

    ideal_dcg = dcg_at_k(
        ideal_results,
        relevant_docs,
        k
    )

    if ideal_dcg == 0:
        return 0.0

    return actual_dcg / ideal_dcg


def main():

    print("=" * 60)
    print("IndicSeek - BM25 Evaluation")
    print("=" * 60)

    documents = load_documents()

    print(f"\nDocuments loaded: {len(documents)}")

    tokenized_documents = [
        tokenize(document["text"])
        for document in documents
    ]

    bm25 = BM25Okapi(tokenized_documents)

    queries = load_queries()

    print(f"Evaluation queries: {len(queries)}")

    reciprocal_ranks = []
    recalls = []
    ndcgs = []

    for item in queries:

        query = item["query"]
        relevant_docs = item["relevant_docs"]

        results = search(
            bm25,
            documents,
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

        ndcg = ndcg_at_k(
            results,
            relevant_docs,
            k=5
        )

        reciprocal_ranks.append(rr)
        recalls.append(recall)
        ndcgs.append(ndcg)

        print("\n" + "-" * 60)
        print(f"Query: {query}")
        print(f"Relevant: {relevant_docs}")

        print(f"Reciprocal Rank: {rr:.4f}")
        print(f"Recall@5:        {recall:.4f}")
        print(f"nDCG@5:          {ndcg:.4f}")

    mrr = sum(reciprocal_ranks) / len(reciprocal_ranks)
    mean_recall = sum(recalls) / len(recalls)
    mean_ndcg = sum(ndcgs) / len(ndcgs)

    print("\n" + "=" * 60)
    print("FINAL BM25 RESULTS")
    print("=" * 60)

    print(f"MRR@5:    {mrr:.4f}")
    print(f"Recall@5: {mean_recall:.4f}")
    print(f"nDCG@5:   {mean_ndcg:.4f}")

    print("=" * 60)


if __name__ == "__main__":
    main()