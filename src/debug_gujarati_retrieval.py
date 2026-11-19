import os
import re
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


# ---------------------------------------------------------
# LOAD DOCUMENTS
# ---------------------------------------------------------

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


# ---------------------------------------------------------
# EXTRACT GUJARATI
# ---------------------------------------------------------

gujarati_docs = []

for doc in documents:

    gujarati = extract_language(
        doc["text"],
        "Gujarati"
    )

    gujarati_docs.append(
        gujarati
    )


# ---------------------------------------------------------
# BUILD BM25
# ---------------------------------------------------------

tokenized_docs = [
    tokenize(text)
    for text in gujarati_docs
]

bm25 = BM25Okapi(
    tokenized_docs
)


# ---------------------------------------------------------
# DENSE MODEL
# ---------------------------------------------------------

print("Loading multilingual model...")

model = SentenceTransformer(
    MODEL_NAME
)

print("Encoding Gujarati documents...")

embeddings = model.encode(
    gujarati_docs,
    convert_to_numpy=True,
    show_progress_bar=True
)


# ---------------------------------------------------------
# QUERY
# ---------------------------------------------------------

query = "શિષ્યવૃત્તિ માટે કયા દસ્તાવેજો જરૂરી છે?"

print("\n" + "=" * 70)
print("GUJARATI RETRIEVAL DEBUG")
print("=" * 70)

print("\nQuery:")
print(query)


# ---------------------------------------------------------
# BM25
# ---------------------------------------------------------

bm25_scores = bm25.get_scores(
    tokenize(query)
)

bm25_rank = np.argsort(
    bm25_scores
)[::-1]


print("\n" + "=" * 70)
print("TOP 10 BM25")
print("=" * 70)

for rank, index in enumerate(
    bm25_rank[:10],
    1
):

    print(
        f"\n{rank}. "
        f"{documents[index]['id']} "
        f"score={bm25_scores[index]:.4f}"
    )

    print(
        gujarati_docs[index]
    )


# ---------------------------------------------------------
# DENSE
# ---------------------------------------------------------

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
    doc_norms * query_norm + 1e-10
)

dense_rank = np.argsort(
    dense_scores
)[::-1]


print("\n" + "=" * 70)
print("TOP 10 DENSE")
print("=" * 70)

for rank, index in enumerate(
    dense_rank[:10],
    1
):

    print(
        f"\n{rank}. "
        f"{documents[index]['id']} "
        f"score={dense_scores[index]:.4f}"
    )

    print(
        gujarati_docs[index]
    )


# ---------------------------------------------------------
# HYBRID
# ---------------------------------------------------------

bm25_norm = normalize(
    bm25_scores
)

dense_norm = normalize(
    dense_scores
)

hybrid_scores = (
    0.5 * bm25_norm
    +
    0.5 * dense_norm
)

hybrid_rank = np.argsort(
    hybrid_scores
)[::-1]


print("\n" + "=" * 70)
print("TOP 10 HYBRID")
print("=" * 70)

for rank, index in enumerate(
    hybrid_rank[:10],
    1
):

    print(
        f"\n{rank}. "
        f"{documents[index]['id']} "
        f"score={hybrid_scores[index]:.4f}"
    )

    print(
        gujarati_docs[index]
    )


print("\n" + "=" * 70)
print("DEBUG COMPLETED")
print("=" * 70)