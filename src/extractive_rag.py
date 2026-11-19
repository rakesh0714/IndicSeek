import os
import re
import json
import numpy as np

from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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

EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"


# =========================================================
# LOAD DOCUMENTS
# =========================================================

def load_documents():

    documents = []

    for filename in sorted(os.listdir(DOC_DIR)):

        if not filename.endswith(".txt"):
            continue

        path = os.path.join(DOC_DIR, filename)

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as f:

            text = f.read()

        documents.append({
            "id": filename.replace(".txt", ""),
            "text": text
        })

    return documents


# =========================================================
# LANGUAGE DETECTION
# =========================================================

def detect_language(text):

    if re.search(r"[\u0A80-\u0AFF]", text):
        return "Gujarati"

    if re.search(r"[\u0900-\u097F]", text):
        return "Hindi"

    return "English"


# =========================================================
# EXTRACT LANGUAGE SECTION
# =========================================================

def extract_language(text, language):

    sections = re.split(
        r"\n(?=(?:ENGLISH|HINDI|GUJARATI)\s*:)",
        text,
        flags=re.IGNORECASE
    )

    for section in sections:

        if section.upper().startswith(language.upper()):

            parts = section.split(":", 1)

            if len(parts) == 2:
                return parts[1].strip()

    return text.strip()


# =========================================================
# TOKENIZATION
# =========================================================

def tokenize(text):

    return re.findall(
        r"\w+",
        text.lower(),
        flags=re.UNICODE
    )


# =========================================================
# NORMALIZATION
# =========================================================

def normalize(scores):

    scores = np.array(scores, dtype=float)

    if scores.max() == scores.min():
        return np.ones_like(scores)

    return (
        (scores - scores.min())
        /
        (scores.max() - scores.min())
    )


# =========================================================
# COSINE SIMILARITY
# =========================================================

def cosine_similarity(query_embedding, document_embeddings):

    query_norm = np.linalg.norm(query_embedding)

    document_norms = np.linalg.norm(
        document_embeddings,
        axis=1
    )

    return np.dot(
        document_embeddings,
        query_embedding
    ) / (
        document_norms * query_norm + 1e-10
    )


# =========================================================
# BUILD RETRIEVER
# =========================================================

def build_retriever(documents):

    texts = [
        doc["text"]
        for doc in documents
    ]

    tokenized_docs = [
        tokenize(text)
        for text in texts
    ]

    bm25 = BM25Okapi(tokenized_docs)

    model = SentenceTransformer(
        EMBEDDING_MODEL
    )

    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        show_progress_bar=True
    )

    return bm25, model, embeddings


# =========================================================
# RETRIEVE
# =========================================================

def retrieve(
    query,
    documents,
    bm25,
    model,
    embeddings,
    top_k=3,
    alpha=0.5
):

    query_tokens = tokenize(query)

    bm25_scores = bm25.get_scores(
        query_tokens
    )

    query_embedding = model.encode(
        [query],
        convert_to_numpy=True
    )[0]

    dense_scores = cosine_similarity(
        query_embedding,
        embeddings
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

    results = []

    language = detect_language(query)

    for index in ranking[:top_k]:

        evidence = extract_language(
            documents[index]["text"],
            language
        )

        results.append({
            "id": documents[index]["id"],
            "score": float(hybrid_scores[index]),
            "evidence": evidence
        })

    return results, language


# =========================================================
# EXTRACTIVE ANSWER
# =========================================================

def create_answer(query, results, language):

    if not results:
        return "No relevant evidence was found."

    # Use the highest-ranked evidence.
    evidence = results[0]["evidence"]

    # Split into sentences.
    sentences = re.split(
        r"(?<=[.!?।॥])\s+",
        evidence
    )

    sentences = [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]

    # Return the most relevant evidence sentence(s).
    if len(sentences) >= 2:
        return " ".join(sentences[:2])

    return evidence


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    print("=" * 70)
    print("IndicSeek - Extractive RAG")
    print("=" * 70)

    documents = load_documents()

    print(f"\nDocuments loaded: {len(documents)}")

    print("\nBuilding retriever...")

    bm25, model, embeddings = build_retriever(
        documents
    )

    print("\nRetriever ready.")

    print("\nType 'exit' to stop.")

    while True:

        query = input("\nQuery: ").strip()

        if query.lower() == "exit":
            break

        if not query:
            continue

        results, language = retrieve(
            query,
            documents,
            bm25,
            model,
            embeddings,
            top_k=3,
            alpha=0.5
        )

        answer = create_answer(
            query,
            results,
            language
        )

        print("\n" + "=" * 70)
        print("LANGUAGE:", language)
        print("=" * 70)

        print("\nANSWER:")
        print(answer)

        print("\nSOURCES:")

        for i, result in enumerate(
            results,
            1
        ):

            print(
                f"\n{i}. {result['id']} "
                f"(score={result['score']:.4f})"
            )

            print(
                result["evidence"]
            )