import os
import re
import json
import numpy as np

from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DOC_DIR = os.path.join(
    BASE_DIR,
    "data",
    "dev_documents"
)

QUERY_FILE = os.path.join(
    BASE_DIR,
    "data",
    "dev_queries.json"
)

MODEL_NAME = (
    "sentence-transformers/"
    "paraphrase-multilingual-mpnet-base-v2"
)


def tokenize(text):
    return re.findall(
        r"\w+",
        text.lower(),
        flags=re.UNICODE
    )


def extract_language(text, language):

    sections = re.split(
        r"\n(?=(?:ENGLISH|HINDI|GUJARATI)\s*:)",
        text,
        flags=re.IGNORECASE
    )

    for section in sections:

        if section.upper().startswith(
            language.upper()
        ):

            parts = section.split(":", 1)

            if len(parts) == 2:
                return parts[1].strip()

    return text.strip()


def normalize(scores):

    scores = np.array(
        scores,
        dtype=float
    )

    if scores.max() == scores.min():
        return np.ones_like(scores)

    return (
        (scores - scores.min())
        /
        (scores.max() - scores.min())
    )


def reciprocal_rank(ranking, relevant):

    for rank, index in enumerate(
        ranking,
        start=1
    ):

        if index in relevant:
            return 1.0 / rank

    return 0.0


# =========================================================
# LOAD DOCUMENTS
# =========================================================

documents = []

for filename in sorted(
    os.listdir(DOC_DIR)
):

    if not filename.endswith(".txt"):
        continue

    with open(
        os.path.join(DOC_DIR, filename),
        "r",
        encoding="utf-8"
    ) as f:

        text = f.read()

    documents.append({
        "id": filename.replace(".txt", ""),
        "text": text
    })


# =========================================================
# LOAD QUERIES
# =========================================================

with open(
    QUERY_FILE,
    "r",
    encoding="utf-8"
) as f:

    queries = json.load(f)


# =========================================================
# KEEP ONLY GUJARATI
# =========================================================

gujarati_queries = [
    q for q in queries
    if q.get("language", "").lower()
    == "gujarati"
]

print(
    f"Gujarati queries: "
    f"{len(gujarati_queries)}"
)


# =========================================================
# GUJARATI DOCUMENTS
# =========================================================

gujarati_docs = [
    extract_language(
        doc["text"],
        "Gujarati"
    )
    for doc in documents
]


# =========================================================
# BM25
# =========================================================

tokenized_docs = [
    tokenize(text)
    for text in gujarati_docs
]

bm25 = BM25Okapi(
    tokenized_docs
)


# =========================================================
# DENSE
# =========================================================

print("\nLoading multilingual model...")

model = SentenceTransformer(
    MODEL_NAME
)

print("Encoding documents...")

embeddings = model.encode(
    gujarati_docs,
    convert_to_numpy=True,
    show_progress_bar=True
)


# =========================================================
# ALPHA TEST
# =========================================================

alphas = [
    0.0,
    0.25,
    0.50,
    0.75,
    1.0
]

print("\n" + "=" * 70)
print("GUJARATI ALPHA EVALUATION")
print("=" * 70)


for alpha in alphas:

    reciprocal_ranks = []

    print(
        f"\nTesting alpha = {alpha:.2f}"
    )

    for query_data in gujarati_queries:

        query = query_data["query"]

        relevant_ids = set(
            query_data["relevant_docs"]
        )

        query_tokens = tokenize(
            query
        )

        bm25_scores = bm25.get_scores(
            query_tokens
        )

        query_embedding = model.encode(
            [query],
            convert_to_numpy=True
        )[0]

        query_norm = np.linalg.norm(
            query_embedding
        )

        doc_norms = np.linalg.norm(
            embeddings,
            axis=1
        )

        dense_scores = np.dot(
            embeddings,
            query_embedding
        ) / (
            doc_norms * query_norm
            + 1e-10
        )

        bm25_norm = normalize(
            bm25_scores
        )

        dense_norm = normalize(
            dense_scores
        )

        hybrid_scores = (
            alpha * bm25_norm
            +
            (1 - alpha) * dense_norm
        )

        ranking = np.argsort(
            hybrid_scores
        )[::-1]

        relevant_indices = {
            i
            for i, doc in enumerate(documents)
            if doc["id"] in relevant_ids
        }

        rr = reciprocal_rank(
            ranking[:5],
            relevant_indices
        )

        reciprocal_ranks.append(rr)

    mrr = np.mean(
        reciprocal_ranks
    )

    print(
        f"MRR@5 = {mrr:.4f}"
    )


print("\n" + "=" * 70)
print("EVALUATION COMPLETED")
print("=" * 70)