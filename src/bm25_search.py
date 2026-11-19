import json
import re
from pathlib import Path

from rank_bm25 import BM25Okapi


# --------------------------------------------------
# 1. Paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DOCUMENT_DIR = PROJECT_ROOT / "data" / "documents"
QUERY_FILE = PROJECT_ROOT / "data" / "queries" / "queries.json"


# --------------------------------------------------
# 2. Text preprocessing
# --------------------------------------------------

def tokenize(text):
    """
    Convert text into lowercase word tokens.
    """
    text = text.lower()
    tokens = re.findall(r"\b\w+\b", text)
    return tokens


# --------------------------------------------------
# 3. Load documents
# --------------------------------------------------

def load_documents():
    documents = []

    for file_path in sorted(DOCUMENT_DIR.glob("*.txt")):
        text = file_path.read_text(encoding="utf-8")

        documents.append({
            "id": file_path.stem,
            "text": text
        })

    return documents


# --------------------------------------------------
# 4. Build BM25 index
# --------------------------------------------------

def build_bm25(documents):
    tokenized_documents = [
        tokenize(document["text"])
        for document in documents
    ]

    return BM25Okapi(tokenized_documents)


# --------------------------------------------------
# 5. Search
# --------------------------------------------------

def search(bm25, documents, query, top_k=5):
    query_tokens = tokenize(query)

    scores = bm25.get_scores(query_tokens)

    ranked_indices = scores.argsort()[::-1][:top_k]

    results = []

    for index in ranked_indices:
        results.append({
            "document_id": documents[index]["id"],
            "score": float(scores[index]),
            "text": documents[index]["text"]
        })

    return results


# --------------------------------------------------
# 6. Load evaluation queries
# --------------------------------------------------

def load_queries():
    with open(QUERY_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


# --------------------------------------------------
# 7. Calculate Reciprocal Rank
# --------------------------------------------------

def reciprocal_rank(results, relevant_documents):
    for rank, result in enumerate(results, start=1):

        if result["document_id"] in relevant_documents:
            return 1 / rank

    return 0.0


# --------------------------------------------------
# 8. Main
# --------------------------------------------------

def main():

    print("=" * 60)
    print("IndicSeek - BM25 Baseline")
    print("=" * 60)

    # Load documents
    documents = load_documents()

    print(f"\nDocuments loaded: {len(documents)}")

    # Build index
    bm25 = build_bm25(documents)

    print("BM25 index created successfully.")

    # Load queries
    queries = load_queries()

    print(f"Evaluation queries: {len(queries)}")

    # ----------------------------------------------
    # Evaluate
    # ----------------------------------------------

    reciprocal_ranks = []

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

        reciprocal_ranks.append(rr)

        print("\n" + "-" * 60)
        print(f"Query: {query}")
        print(f"Relevant documents: {relevant_docs}")

        print("\nTop results:")

        for rank, result in enumerate(results, start=1):

            marker = (
                "✓"
                if result["document_id"] in relevant_docs
                else " "
            )

            print(
                f"{rank}. "
                f"{result['document_id']} "
                f"Score={result['score']:.4f} "
                f"{marker}"
            )

    # ----------------------------------------------
    # MRR
    # ----------------------------------------------

    mrr = sum(reciprocal_ranks) / len(reciprocal_ranks)

    print("\n" + "=" * 60)
    print(f"BM25 MRR@5: {mrr:.4f}")
    print("=" * 60)


if __name__ == "__main__":
    main()