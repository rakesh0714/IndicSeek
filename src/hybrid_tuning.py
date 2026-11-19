import json
import re
from pathlib import Path

import numpy as np
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOCUMENT_DIR = PROJECT_ROOT / "data" / "dev_documents"
QUERY_FILE = PROJECT_ROOT / "data" / "dev_queries.json"

MODEL_NAME = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"


def tokenize(text):
    return re.findall(r"\b\w+\b", text.lower())


def load_documents():
    documents = []

    for file_path in sorted(DOCUMENT_DIR.glob("d*.txt")):
        text = file_path.read_text(encoding="utf-8")

        documents.append({
            "id": file_path.stem,
            "text": text
        })

    return documents


def load_queries():
    with open(QUERY_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


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


def reciprocal_rank(ranked_ids, relevant_docs, k=5):
    for rank, document_id in enumerate(
        ranked_ids[:k],
        start=1
    ):
        if document_id in relevant_docs:
            return 1.0 / rank

    return 0.0


def recall_at_k(ranked_ids, relevant_docs, k=5):
    retrieved = set(ranked_ids[:k])
    relevant = set(relevant_docs)

    if not relevant:
        return 0.0

    return len(
        retrieved.intersection(relevant)
    ) / len(relevant)


def dcg(relevances):
    score = 0.0

    for rank, relevance in enumerate(
        relevances,
        start=1
    ):
        score += relevance / np.log2(rank + 1)

    return score


def ndcg_at_k(ranked_ids, relevant_docs, k=5):
    relevant_set = set(relevant_docs)

    actual = [
        1 if document_id in relevant_set else 0
        for document_id in ranked_ids[:k]
    ]

    ideal = sorted(actual, reverse=True)

    actual_dcg = dcg(actual)
    ideal_dcg = dcg(ideal)

    if ideal_dcg == 0:
        return 0.0

    return actual_dcg / ideal_dcg


def evaluate_method(rankings, queries, k=5):

    reciprocal_ranks = []
    recalls = []
    ndcgs = []

    for query, ranking in zip(
        queries,
        rankings
    ):

        relevant_docs = query["relevant_docs"]

        reciprocal_ranks.append(
            reciprocal_rank(
                ranking,
                relevant_docs,
                k
            )
        )

        recalls.append(
            recall_at_k(
                ranking,
                relevant_docs,
                k
            )
        )

        ndcgs.append(
            ndcg_at_k(
                ranking,
                relevant_docs,
                k
            )
        )

    return {
        "MRR@5": np.mean(reciprocal_ranks),
        "Recall@5": np.mean(recalls),
        "nDCG@5": np.mean(ndcgs)
    }


def main():

    print("=" * 70)
    print("IndicSeek - Hybrid Alpha Tuning")
    print("=" * 70)

    documents = load_documents()
    queries = load_queries()

    print(f"\nDocuments: {len(documents)}")
    print(f"Queries:   {len(queries)}")

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
    # Multilingual Dense Model
    # --------------------------------------------------

    print("\nLoading multilingual model...")

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
    # Calculate BM25 and Dense scores
    # --------------------------------------------------

    print("\nCalculating retrieval scores...")

    bm25_scores_all = []
    dense_scores_all = []

    query_texts = [
        query["query"]
        for query in queries
    ]

    query_embeddings = model.encode(
        query_texts,
        convert_to_numpy=True,
        show_progress_bar=True
    )

    for i, query in enumerate(queries):

        # BM25
        query_tokens = tokenize(
            query["query"]
        )

        bm25_scores = bm25.get_scores(
            query_tokens
        )

        # Dense
        dense_scores = cosine_similarity(
            query_embeddings[i],
            document_embeddings
        )

        bm25_scores_all.append(
            bm25_scores
        )

        dense_scores_all.append(
            dense_scores
        )

    # --------------------------------------------------
    # Tune alpha
    # --------------------------------------------------

    alphas = [
        0.00,
        0.25,
        0.50,
        0.75,
        1.00
    ]

    results = []

    print("\n" + "=" * 70)
    print("ALPHA TUNING RESULTS")
    print("=" * 70)

    print(
        f"\n{'Alpha':<10}"
        f"{'MRR@5':>12}"
        f"{'Recall@5':>12}"
        f"{'nDCG@5':>12}"
    )

    print("-" * 46)

    for alpha in alphas:

        rankings = []

        for i in range(len(queries)):

            bm25_normalized = normalize(
                bm25_scores_all[i]
            )

            dense_normalized = normalize(
                dense_scores_all[i]
            )

            hybrid_scores = (
                alpha * bm25_normalized
                + (1 - alpha) * dense_normalized
            )

            ranked_indices = np.argsort(
                hybrid_scores
            )[::-1]

            ranking = [
                documents[index]["id"]
                for index in ranked_indices
            ]

            rankings.append(ranking)

        metrics = evaluate_method(
            rankings,
            queries
        )

        results.append({
            "alpha": alpha,
            **metrics
        })

        print(
            f"{alpha:<10.2f}"
            f"{metrics['MRR@5']:>12.4f}"
            f"{metrics['Recall@5']:>12.4f}"
            f"{metrics['nDCG@5']:>12.4f}"
        )

    # --------------------------------------------------
    # Find best alpha for each metric
    # --------------------------------------------------

    best_mrr = max(
        results,
        key=lambda x: x["MRR@5"]
    )

    best_recall = max(
        results,
        key=lambda x: x["Recall@5"]
    )

    best_ndcg = max(
        results,
        key=lambda x: x["nDCG@5"]
    )

    print("\n" + "=" * 70)
    print("BEST ALPHA BY METRIC")
    print("=" * 70)

    print(
        f"\nBest MRR@5: "
        f"alpha={best_mrr['alpha']:.2f} "
        f"({best_mrr['MRR@5']:.4f})"
    )

    print(
        f"Best Recall@5: "
        f"alpha={best_recall['alpha']:.2f} "
        f"({best_recall['Recall@5']:.4f})"
    )

    print(
        f"Best nDCG@5: "
        f"alpha={best_ndcg['alpha']:.2f} "
        f"({best_ndcg['nDCG@5']:.4f})"
    )

    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()