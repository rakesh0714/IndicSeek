import json
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer, CrossEncoder


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOCUMENT_DIR = PROJECT_ROOT / "data" / "dev_documents"
QUERY_FILE = PROJECT_ROOT / "data" / "dev_queries.json"

DENSE_MODEL = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"

CANDIDATE_K = 10
FINAL_K = 5


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

    mrr = []
    recall = []
    ndcg = []

    for query, ranking in zip(queries, rankings):

        relevant = query["relevant_docs"]

        mrr.append(
            reciprocal_rank(
                ranking,
                relevant,
                k
            )
        )

        recall.append(
            recall_at_k(
                ranking,
                relevant,
                k
            )
        )

        ndcg.append(
            ndcg_at_k(
                ranking,
                relevant,
                k
            )
        )

    return {
        "MRR@5": np.mean(mrr),
        "Recall@5": np.mean(recall),
        "nDCG@5": np.mean(ndcg)
    }


def main():

    print("=" * 70)
    print("IndicSeek - Top-10 Dense Retrieval + Cross-Encoder")
    print("=" * 70)

    documents = load_documents()
    queries = load_queries()

    print(f"\nDocuments: {len(documents)}")
    print(f"Queries:   {len(queries)}")

    # --------------------------------------------------
    # Dense retriever
    # --------------------------------------------------

    print("\nLoading multilingual dense model...")

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

    query_texts = [
        query["query"]
        for query in queries
    ]

    print("Creating query embeddings...")

    query_embeddings = dense_model.encode(
        query_texts,
        convert_to_numpy=True,
        show_progress_bar=True
    )

    # --------------------------------------------------
    # Dense Top-10
    # --------------------------------------------------

    print(
        f"\nRetrieving top-{CANDIDATE_K} candidates..."
    )

    candidate_rankings = []

    for i in range(len(queries)):

        scores = cosine_similarity(
            query_embeddings[i],
            document_embeddings
        )

        ranked_indices = np.argsort(scores)[::-1]

        top_indices = ranked_indices[:CANDIDATE_K]

        candidate_ids = [
            documents[index]["id"]
            for index in top_indices
        ]

        candidate_rankings.append(candidate_ids)

    # --------------------------------------------------
    # Check candidate recall
    # --------------------------------------------------

    candidate_recall = []

    for query, candidates in zip(
        queries,
        candidate_rankings
    ):

        relevant = set(query["relevant_docs"])
        retrieved = set(candidates)

        if relevant:
            value = len(
                relevant.intersection(retrieved)
            ) / len(relevant)
        else:
            value = 0.0

        candidate_recall.append(value)

    print(
        f"\nCandidate Recall@10: "
        f"{np.mean(candidate_recall):.4f}"
    )

    # --------------------------------------------------
    # Load reranker
    # --------------------------------------------------

    print("\nLoading cross-encoder...")

    reranker = CrossEncoder(
        RERANKER_MODEL
    )

    # --------------------------------------------------
    # Rerank Top-10 → Top-5
    # --------------------------------------------------

    print(
        f"\nReranking top-{CANDIDATE_K} "
        f"candidates to top-{FINAL_K}..."
    )

    reranked_rankings = []

    for query, candidate_ids in zip(
        queries,
        candidate_rankings
    ):

        document_lookup = {
            document["id"]: document
            for document in documents
        }

        pairs = []

        for document_id in candidate_ids:

            document = document_lookup[document_id]

            pairs.append([
                query["query"],
                document["text"]
            ])

        scores = reranker.predict(pairs)

        ranked_indices = np.argsort(scores)[::-1]

        top_indices = ranked_indices[:FINAL_K]

        final_ids = [
            candidate_ids[index]
            for index in top_indices
        ]

        reranked_rankings.append(final_ids)

    # --------------------------------------------------
    # Evaluation
    # --------------------------------------------------

    results = evaluate(
        reranked_rankings,
        queries,
        FINAL_K
    )

    print("\n" + "=" * 70)
    print("TOP-10 → RERANK → TOP-5 RESULTS")
    print("=" * 70)

    print(
        f"\nMRR@5:    {results['MRR@5']:.4f}"
    )

    print(
        f"Recall@5: {results['Recall@5']:.4f}"
    )

    print(
        f"nDCG@5:   {results['nDCG@5']:.4f}"
    )

    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()