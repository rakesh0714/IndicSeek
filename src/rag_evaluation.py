import re
from pathlib import Path

import numpy as np
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer

from rag_generator import (
    load_documents,
    tokenize,
    retrieve,
    detect_language,
    extract_language,
    load_generator,
    generate_answer,
)


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DOCUMENT_DIR = PROJECT_ROOT / "data" / "dev_documents"


# ============================================================
# MODELS
# ============================================================

RETRIEVER_MODEL = (
    "sentence-transformers/"
    "paraphrase-multilingual-mpnet-base-v2"
)


# ============================================================
# SETTINGS
# ============================================================

TOP_K = 3


# ============================================================
# COSINE SIMILARITY
# ============================================================

def cosine_similarity(a, b):

    a_norm = np.linalg.norm(a)
    b_norm = np.linalg.norm(b)

    if a_norm == 0 or b_norm == 0:
        return 0.0

    return float(
        np.dot(a, b)
        / (a_norm * b_norm)
    )


# ============================================================
# ANSWER RELEVANCE
# ============================================================

def calculate_answer_relevance(
    query,
    answer,
    model
):

    query_embedding = model.encode(
        query,
        convert_to_numpy=True
    )

    answer_embedding = model.encode(
        answer,
        convert_to_numpy=True
    )

    return cosine_similarity(
        query_embedding,
        answer_embedding
    )


# ============================================================
# EVIDENCE COVERAGE
# ============================================================

def calculate_evidence_coverage(
    answer,
    evidence
):

    answer_words = set(
        re.findall(
            r"\b\w+\b",
            answer.lower()
        )
    )

    if not answer_words:
        return 0.0

    evidence_text = " ".join(
        evidence
    ).lower()

    evidence_words = set(
        re.findall(
            r"\b\w+\b",
            evidence_text
        )
    )

    overlap = (
        answer_words
        & evidence_words
    )

    return len(overlap) / len(
        answer_words
    )


# ============================================================
# GROUNDEDNESS
# ============================================================

def calculate_groundedness(
    answer,
    evidence,
    model
):

    if not answer.strip():
        return 0.0

    answer_embedding = model.encode(
        answer,
        convert_to_numpy=True
    )

    evidence_embeddings = model.encode(
        evidence,
        convert_to_numpy=True
    )

    similarities = []

    for evidence_embedding in evidence_embeddings:

        score = cosine_similarity(
            answer_embedding,
            evidence_embedding
        )

        similarities.append(score)

    if not similarities:
        return 0.0

    return max(similarities)


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print("IndicSeek - ACTUAL RAG EVALUATION")
    print("=" * 70)

    # --------------------------------------------------------
    # Load documents
    # --------------------------------------------------------

    documents = load_documents()

    print(
        f"\nDocuments loaded: {len(documents)}"
    )

    # --------------------------------------------------------
    # Build BM25
    # --------------------------------------------------------

    print(
        "\nBuilding BM25 index..."
    )

    tokenized_documents = [
        tokenize(document["text"])
        for document in documents
    ]

    bm25 = BM25Okapi(
        tokenized_documents
    )

    print(
        "BM25 index created."
    )

    # --------------------------------------------------------
    # Load retriever
    # --------------------------------------------------------

    print(
        "\nLoading multilingual retriever..."
    )

    retriever = SentenceTransformer(
        RETRIEVER_MODEL
    )

    print(
        "Retriever loaded."
    )

    # --------------------------------------------------------
    # Document embeddings
    # --------------------------------------------------------

    document_texts = [
        document["text"]
        for document in documents
    ]

    print(
        "\nCreating document embeddings..."
    )

    document_embeddings = retriever.encode(
        document_texts,
        convert_to_numpy=True,
        show_progress_bar=True
    )

    print(
        f"Embedding shape: "
        f"{document_embeddings.shape}"
    )

    # --------------------------------------------------------
    # Load actual FLAN-T5 generator
    # --------------------------------------------------------

    tokenizer, generator_model, device = (
        load_generator()
    )

    # --------------------------------------------------------
    # Test query
    # --------------------------------------------------------

    print("\n" + "=" * 70)

    query = input(
        "\nEnter query for RAG evaluation: "
    ).strip()

    if not query:

        print(
            "Query cannot be empty."
        )

        return

    # --------------------------------------------------------
    # Detect language
    # --------------------------------------------------------

    language = detect_language(
        query
    )

    print(
        f"\nDetected language: {language}"
    )

    # --------------------------------------------------------
    # Retrieve
    # --------------------------------------------------------

    print(
        "\nRetrieving evidence..."
    )

    ranked_indices = retrieve(
        query,
        documents,
        bm25,
        document_embeddings,
        retriever
    )

    # --------------------------------------------------------
    # Extract evidence
    # --------------------------------------------------------

    evidence = []

    for rank, index in enumerate(
        ranked_indices,
        start=1
    ):

        document = documents[index]

        text = extract_language(
            document["text"],
            language
        )

        evidence.append(
            {
                "rank": rank,
                "id": document["id"],
                "text": text
            }
        )

    # --------------------------------------------------------
    # Evidence text
    # --------------------------------------------------------

    evidence_texts = [
        item["text"]
        for item in evidence
    ]

    # --------------------------------------------------------
    # Generate ACTUAL answer
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("GENERATING ACTUAL RAG ANSWER...")
    print("=" * 70)

    context = ""

    for item in evidence:

        context += (
            f"\nSource {item['id']}:\n"
            f"{item['text']}\n"
        )

    answer = generate_answer(
        query,
        context,
        language,
        tokenizer,
        generator_model,
        device
    )

    # --------------------------------------------------------
    # Calculate metrics
    # --------------------------------------------------------

    print(
        "\nCalculating Answer Relevance..."
    )

    relevance = calculate_answer_relevance(
        query,
        answer,
        retriever
    )

    print(
        "Calculating Evidence Coverage..."
    )

    coverage = calculate_evidence_coverage(
        answer,
        evidence_texts
    )

    print(
        "Calculating Groundedness..."
    )

    groundedness = calculate_groundedness(
        answer,
        evidence_texts,
        retriever
    )

    overall_score = (
        relevance
        + coverage
        + groundedness
    ) / 3

    # --------------------------------------------------------
    # Display answer
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("RAG ANSWER")
    print("=" * 70)

    print(
        f"\n{answer}"
    )

    # --------------------------------------------------------
    # Display evidence
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("RETRIEVED EVIDENCE")
    print("=" * 70)

    for item in evidence:

        print(
            f"\nRank {item['rank']}"
        )

        print(
            f"Document: {item['id']}"
        )

        print(
            f"Evidence: {item['text']}"
        )

    # --------------------------------------------------------
    # Evaluation results
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("ACTUAL RAG EVALUATION RESULTS")
    print("=" * 70)

    print(
        f"\nAnswer Relevance : "
        f"{relevance:.4f}"
    )

    print(
        f"Evidence Coverage: "
        f"{coverage:.4f}"
    )

    print(
        f"Groundedness     : "
        f"{groundedness:.4f}"
    )

    print(
        f"Overall RAG Score: "
        f"{overall_score:.4f}"
    )

    # --------------------------------------------------------
    # Sources
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("SOURCES")
    print("=" * 70)

    for item in evidence:

        print(
            f"{item['rank']}. "
            f"{item['id']}"
        )

    print("\n" + "=" * 70)
    print("Actual RAG evaluation completed.")
    print("=" * 70)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()