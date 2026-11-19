import re
from pathlib import Path

import numpy as np
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOCUMENT_DIR = PROJECT_ROOT / "data" / "dev_documents"

MODEL_NAME = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"

TOP_K = 3
ALPHA = 0.50


def tokenize(text):
    return re.findall(r"\b\w+\b", text.lower())


def load_documents():
    documents = []

    for file_path in sorted(DOCUMENT_DIR.glob("d*.txt")):
        documents.append({
            "id": file_path.stem,
            "text": file_path.read_text(encoding="utf-8")
        })

    return documents


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


def extract_english(text):
    match = re.search(
        r"English:\s*(.*?)(?=\nHindi:|\nGujarati:|$)",
        text,
        re.DOTALL
    )

    if match:
        return match.group(1).strip()

    return text.strip()


def extract_language(text, language):

    if language.lower() == "english":
        return extract_english(text)

    if language.lower() == "hindi":
        pattern = r"Hindi:\s*(.*?)(?=\nGujarati:|$)"

    elif language.lower() == "gujarati":
        pattern = r"Gujarati:\s*(.*)$"

    else:
        return text.strip()

    match = re.search(
        pattern,
        text,
        re.DOTALL
    )

    if match:
        return match.group(1).strip()

    return text.strip()


def detect_language(query):

    hindi_chars = len(
        re.findall(r"[\u0900-\u097F]", query)
    )

    gujarati_chars = len(
        re.findall(r"[\u0A80-\u0AFF]", query)
    )

    if hindi_chars > gujarati_chars and hindi_chars > 0:
        return "Hindi"

    if gujarati_chars > hindi_chars and gujarati_chars > 0:
        return "Gujarati"

    return "English"


def retrieve(query, documents, bm25, document_embeddings, model):

    query_tokens = tokenize(query)

    bm25_scores = bm25.get_scores(
        query_tokens
    )

    query_embedding = model.encode(
        query,
        convert_to_numpy=True
    )

    dense_scores = cosine_similarity(
        query_embedding,
        document_embeddings
    )

    bm25_normalized = normalize(
        bm25_scores
    )

    dense_normalized = normalize(
        dense_scores
    )

    hybrid_scores = (
        ALPHA * bm25_normalized
        + (1 - ALPHA) * dense_normalized
    )

    ranked_indices = np.argsort(
        hybrid_scores
    )[::-1]

    return ranked_indices[:TOP_K]


def main():

    print("=" * 70)
    print("IndicSeek - Evidence-Grounded RAG Pipeline")
    print("=" * 70)

    documents = load_documents()

    print(f"\nDocuments loaded: {len(documents)}")

    # --------------------------------------------------
    # Build retrieval system
    # --------------------------------------------------

    print("\nBuilding BM25 index...")

    tokenized_documents = [
        tokenize(document["text"])
        for document in documents
    ]

    bm25 = BM25Okapi(
        tokenized_documents
    )

    print("\nLoading multilingual model...")

    model = SentenceTransformer(
        MODEL_NAME
    )

    document_texts = [
        document["text"]
        for document in documents
    ]

    print("\nCreating document embeddings...")

    document_embeddings = model.encode(
        document_texts,
        convert_to_numpy=True,
        show_progress_bar=True
    )

    # --------------------------------------------------
    # Query
    # --------------------------------------------------

    print("\n" + "=" * 70)

    query = input(
        "\nEnter your query: "
    ).strip()

    if not query:
        print("Query cannot be empty.")
        return

    language = detect_language(query)

    print(
        f"\nDetected language: {language}"
    )

    # --------------------------------------------------
    # Retrieval
    # --------------------------------------------------

    ranked_indices = retrieve(
        query,
        documents,
        bm25,
        document_embeddings,
        model
    )

    # --------------------------------------------------
    # Build evidence context
    # --------------------------------------------------

    evidence = []

    for rank, index in enumerate(
        ranked_indices,
        start=1
    ):

        document = documents[index]

        relevant_text = extract_language(
            document["text"],
            language
        )

        evidence.append({
            "rank": rank,
            "document_id": document["id"],
            "text": relevant_text
        })

    # --------------------------------------------------
    # Display evidence
    # --------------------------------------------------

    print("\n" + "=" * 70)
    print("RETRIEVED EVIDENCE FOR RAG")
    print("=" * 70)

    for item in evidence:

        print(
            f"\n[{item['rank']}] "
            f"Source: {item['document_id']}"
        )

        print(
            item["text"]
        )

        print("-" * 70)

    # --------------------------------------------------
    # Build context
    # --------------------------------------------------

    context_parts = []

    for item in evidence:

        context_parts.append(
            f"[Source {item['document_id']}]\n"
            f"{item['text']}"
        )

    context = "\n\n".join(
        context_parts
    )

    # --------------------------------------------------
    # RAG prompt
    # --------------------------------------------------

    prompt = f"""
You are an evidence-grounded assistant.

Answer the user's question using ONLY the
provided evidence.

If the evidence does not contain enough
information, say that the available evidence
is insufficient.

Do not invent information.

User question:
{query}

Evidence:
{context}

Answer:
"""

    print("\n" + "=" * 70)
    print("RAG PROMPT")
    print("=" * 70)

    print(prompt)

    print("=" * 70)


if __name__ == "__main__":
    main()