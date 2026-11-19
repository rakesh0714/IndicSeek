import json
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

QUERY_FILE = PROJECT_ROOT / "data" / "dev_queries.json"


# ============================================================
# MODEL
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
# LOAD QUERIES
# ============================================================

def load_queries():

    with open(
        QUERY_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        data = json.load(file)

    # Support different possible JSON structures

    if isinstance(data, list):
        return data

    if isinstance(data, dict):

        if "queries" in data:
            return data["queries"]

        if "data" in data:
            return data["data"]

    raise ValueError(
        "Unsupported dev_queries.json format."
    )


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
# GET QUERY TEXT
# ============================================================

def get_query_text(item):

    if isinstance(item, str):
        return item

    if isinstance(item, dict):

        possible_keys = [
            "query",
            "question",
            "text",
            "query_text"
        ]

        for key in possible_keys:

            if key in item:

                return str(
                    item[key]
                )

    return ""


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print("IndicSeek - FULL RAG EVALUATION")
    print("=" * 70)

    # --------------------------------------------------------
    # Load queries
    # --------------------------------------------------------

    queries = load_queries()

    print(
        f"\nQueries loaded: {len(queries)}"
    )

    # --------------------------------------------------------
    # Load documents
    # --------------------------------------------------------

    documents = load_documents()

    print(
        f"Documents loaded: {len(documents)}"
    )

    # --------------------------------------------------------
    # BM25
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
    # Retriever
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

    print(
        "\nCreating document embeddings..."
    )

    document_texts = [
        document["text"]
        for document in documents
    ]

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
    # Generator
    # --------------------------------------------------------

    print(
        "\nLoading FLAN-T5 generator..."
    )

    tokenizer, generator_model, device = (
        load_generator()
    )

    # --------------------------------------------------------
    # Results
    # --------------------------------------------------------

    results = []

    # --------------------------------------------------------
    # Evaluate every query
    # --------------------------------------------------------

    for query_number, item in enumerate(
        queries,
        start=1
    ):

        query = get_query_text(
            item
        )

        if not query:
            continue

        print("\n" + "=" * 70)

        print(
            f"QUERY {query_number}/{len(queries)}"
        )

        print(
            f"Question: {query}"
        )

        # ----------------------------------------------------
        # Language
        # ----------------------------------------------------

        language = detect_language(
            query
        )

        print(
            f"Language: {language}"
        )

        # ----------------------------------------------------
        # Retrieval
        # ----------------------------------------------------

        ranked_indices = retrieve(
            query,
            documents,
            bm25,
            document_embeddings,
            retriever
        )

        # ----------------------------------------------------
        # Evidence
        # ----------------------------------------------------

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

        evidence_texts = [
            item["text"]
            for item in evidence
        ]

        # ----------------------------------------------------
        # Context
        # ----------------------------------------------------

        context = ""

        for evidence_item in evidence:

            context += (
                f"\nSource "
                f"{evidence_item['id']}:\n"
                f"{evidence_item['text']}\n"
            )

        # ----------------------------------------------------
        # Generate actual answer
        # ----------------------------------------------------

        print(
            "\nGenerating answer..."
        )

        answer = generate_answer(
            query,
            context,
            language,
            tokenizer,
            generator_model,
            device
        )

        # ----------------------------------------------------
        # Metrics
        # ----------------------------------------------------

        relevance = (
            calculate_answer_relevance(
                query,
                answer,
                retriever
            )
        )

        coverage = (
            calculate_evidence_coverage(
                answer,
                evidence_texts
            )
        )

        groundedness = (
            calculate_groundedness(
                answer,
                evidence_texts,
                retriever
            )
        )

        overall = (
            relevance
            + coverage
            + groundedness
        ) / 3

        # ----------------------------------------------------
        # Store
        # ----------------------------------------------------

        results.append(
            {
                "query_number": query_number,
                "query": query,
                "language": language,
                "answer": answer,
                "sources": [
                    item["id"]
                    for item in evidence
                ],
                "answer_relevance": relevance,
                "evidence_coverage": coverage,
                "groundedness": groundedness,
                "overall_score": overall
            }
        )

        # ----------------------------------------------------
        # Display
        # ----------------------------------------------------

        print(
            f"\nAnswer: {answer}"
        )

        print(
            "\nSources: "
            + ", ".join(
                item["id"]
                for item in evidence
            )
        )

        print(
            f"\nRelevance:    {relevance:.4f}"
        )

        print(
            f"Coverage:     {coverage:.4f}"
        )

        print(
            f"Groundedness: {groundedness:.4f}"
        )

        print(
            f"Overall:      {overall:.4f}"
        )

    # ========================================================
    # FINAL RESULTS
    # ========================================================

    if not results:

        print(
            "\nNo results were generated."
        )

        return

    average_relevance = np.mean(
        [
            result["answer_relevance"]
            for result in results
        ]
    )

    average_coverage = np.mean(
        [
            result["evidence_coverage"]
            for result in results
        ]
    )

    average_groundedness = np.mean(
        [
            result["groundedness"]
            for result in results
        ]
    )

    average_overall = np.mean(
        [
            result["overall_score"]
            for result in results
        ]
    )

    # --------------------------------------------------------
    # Final report
    # --------------------------------------------------------

    print("\n\n" + "=" * 70)
    print("FINAL RAG EVALUATION")
    print("=" * 70)

    print(
        f"\nQueries evaluated: "
        f"{len(results)}"
    )

    print(
        f"\nAverage Answer Relevance : "
        f"{average_relevance:.4f}"
    )

    print(
        f"Average Evidence Coverage: "
        f"{average_coverage:.4f}"
    )

    print(
        f"Average Groundedness     : "
        f"{average_groundedness:.4f}"
    )

    print(
        f"Average Overall Score    : "
        f"{average_overall:.4f}"
    )

    # --------------------------------------------------------
    # Language-wise evaluation
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("LANGUAGE-WISE RESULTS")
    print("=" * 70)

    languages = sorted(
        set(
            result["language"]
            for result in results
        )
    )

    for language in languages:

        language_results = [
            result
            for result in results
            if result["language"] == language
        ]

        language_relevance = np.mean(
            [
                result["answer_relevance"]
                for result in language_results
            ]
        )

        language_coverage = np.mean(
            [
                result["evidence_coverage"]
                for result in language_results
            ]
        )

        language_groundedness = np.mean(
            [
                result["groundedness"]
                for result in language_results
            ]
        )

        language_overall = np.mean(
            [
                result["overall_score"]
                for result in language_results
            ]
        )

        print(
            f"\n{language}"
        )

        print(
            f"Queries: {len(language_results)}"
        )

        print(
            f"Relevance: "
            f"{language_relevance:.4f}"
        )

        print(
            f"Coverage: "
            f"{language_coverage:.4f}"
        )

        print(
            f"Groundedness: "
            f"{language_groundedness:.4f}"
        )

        print(
            f"Overall: "
            f"{language_overall:.4f}"
        )

    # --------------------------------------------------------
    # Save results
    # --------------------------------------------------------

    output_file = (
        PROJECT_ROOT
        / "evaluation"
        / "rag_results.json"
    )

    output_file.parent.mkdir(
        exist_ok=True
    )

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            results,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(
        f"\nDetailed results saved to:"
    )

    print(
        output_file
    )

    print("\n" + "=" * 70)
    print("FULL RAG EVALUATION COMPLETED")
    print("=" * 70)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()  