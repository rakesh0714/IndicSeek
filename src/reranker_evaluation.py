import json
import re
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer, CrossEncoder


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOCUMENT_DIR = PROJECT_ROOT / "data" / "dev_documents"
QUERY_FILE = PROJECT_ROOT / "data" / "dev_queries.json"

DENSE_MODEL = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"

TOP_K_RETRIEVAL = 5
TOP_K_EVALUATION = 5


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


def evaluate(rankings, queries, k=5):

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
    print("IndicSeek - Dense Retrieval + Cross-Encoder Reranking")
    print("=" * 70)

    documents = load_documents()
    queries = load_queries()

    print(f"\nDocuments: {len(documents)}")
    print(f"Queries:   {len(queries)}")

    # --------------------------------------------------
    # Load Dense Retriever
    # --------------------------------------------------

    print("\nLoading multilingual dense retriever...")

    dense_model = SentenceTransformer(DENSE_MODEL)

    document_texts = [
        document["text"]
        for document in documents
    ]

    print("Creating document embeddings...")

    document_embeddings = dense_model.encode(
        document_texts,
        convert_to_numpy=True,
        show_progress_bar=True
    )

    # --------------------------------------------------
    # Generate Dense Rankings
    # --------------------------------------------------

    print("\nGenerating dense retrieval candidates...")

    query_texts = [
        query["query"]
        for query in queries
    ]

    query_embeddings = dense_model.encode(
        query_texts,
        convert_to_numpy=True,
        show_progress_bar=True
    )

    candidate_rankings = []

    for i, query in enumerate(queries):

        scores = cosine_similarity(
            query_embeddings[i],
            document_embeddings
        )

        ranked_indices = np.argsort(scores)[::-1]

        top_indices = ranked_indices[:TOP_K_RETRIEVAL]

        ranking = [
            documents[index]["id"]
            for index in top_indices
        ]

        candidate_rankings.append(ranking)

    # --------------------------------------------------
    # Evaluate Dense Retrieval
    # --------------------------------------------------

    dense_results = evaluate(
        candidate_rankings,
        queries,
        TOP_K_EVALUATION
    )

    print("\n" + "=" * 70)
    print("DENSE RETRIEVAL RESULTS")
    print("=" * 70)

    print(
        f"MRR@5:    {dense_results['MRR@5']:.4f}"
    )

    print(
        f"Recall@5: {dense_results['Recall@5']:.4f}"
    )

    print(
        f"nDCG@5:   {dense_results['nDCG@5']:.4f}"
    )

    # --------------------------------------------------
    # Load Cross Encoder
    # --------------------------------------------------

    print("\nLoading cross-encoder reranker...")

    reranker = CrossEncoder(
        RERANKER_MODEL
    )

    # --------------------------------------------------
    # Rerank Candidates
    # --------------------------------------------------

    print("\nReranking candidates...")

    reranked_rankings = []

    for query, candidate_ids in zip(
        queries,
        candidate_rankings
    ):

        pairs = []

        candidate_documents = []

        for document_id in candidate_ids:

            document = next(
                document
                for document in documents
                if document["id"] == document_id
            )

            pairs.append(
                [
                    query["query"],
                    document["text"]
                ]
            )

            candidate_documents.append(
                document
            )

        reranker_scores = reranker.predict(
            pairs
        )

        ranked_order = np.argsort(
            reranker_scores
        )[::-1]

        reranked_ids = [
            candidate_documents[index]["id"]
            for index in ranked_order
        ]

        reranked_rankings.append(
            reranked_ids
        )

    # --------------------------------------------------
    # Evaluate Reranked Results
    # --------------------------------------------------

    reranker_results = evaluate(
        reranked_rankings,
        queries,
        TOP_K_EVALUATION
    )

    print("\n" + "=" * 70)
    print("RERANKED RESULTS")
    print("=" * 70)

    print(
        f"MRR@5:    {reranker_results['MRR@5']:.4f}"
    )

    print(
        f"Recall@5: {reranker_results['Recall@5']:.4f}"
    )

    print(
        f"nDCG@5:   {reranker_results['nDCG@5']:.4f}"
    )

    # --------------------------------------------------
    # Comparison
    # --------------------------------------------------

    print("\n" + "=" * 70)
    print("DENSE vs RERANKER")
    print("=" * 70)

    print(
        f"\n{'Metric':<15}"
        f"{'Dense':>12}"
        f"{'Reranked':>12}"
        f"{'Change':>12}"
    )

    print("-" * 51)

    metrics = [
        "MRR@5",
        "Recall@5",
        "nDCG@5"
    ]

    for metric in metrics:

        dense_value = dense_results[metric]
        reranked_value = reranker_results[metric]

        change = reranked_value - dense_value

        print(
            f"{metric:<15}"
            f"{dense_value:>12.4f}"
            f"{reranked_value:>12.4f}"
            f"{change:>+12.4f}"
        )

    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()