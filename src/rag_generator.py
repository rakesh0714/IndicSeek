import re
from pathlib import Path

import numpy as np
import torch
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


# ============================================================
# PATHS AND MODELS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DOCUMENT_DIR = PROJECT_ROOT / "data" / "dev_documents"

RETRIEVER_MODEL = (
    "sentence-transformers/"
    "paraphrase-multilingual-mpnet-base-v2"
)

GENERATOR_MODEL = "google/flan-t5-base"

TOP_K = 3
ALPHA = 0.50


# ============================================================
# TEXT TOKENIZATION
# ============================================================

def tokenize(text):
    """
    Tokenize text for BM25.
    """
    return re.findall(
        r"\b\w+\b",
        text.lower(),
        flags=re.UNICODE
    )


# ============================================================
# LOAD DOCUMENTS
# ============================================================

def load_documents():
    """
    Load all development documents.
    """

    documents = []

    for file_path in sorted(
        DOCUMENT_DIR.glob("d*.txt")
    ):
        documents.append(
            {
                "id": file_path.stem,
                "text": file_path.read_text(
                    encoding="utf-8"
                )
            }
        )

    return documents


# ============================================================
# SCORE NORMALIZATION
# ============================================================

def normalize(scores):
    """
    Min-max normalization.
    """

    scores = np.asarray(
        scores,
        dtype=np.float32
    )

    minimum = np.min(scores)
    maximum = np.max(scores)

    if maximum == minimum:
        return np.zeros_like(scores)

    return (
        (scores - minimum)
        / (maximum - minimum)
    )


# ============================================================
# COSINE SIMILARITY
# ============================================================

def cosine_similarity(
    query_embedding,
    document_embeddings
):
    """
    Calculate cosine similarity between
    query embedding and document embeddings.
    """

    query_norm = np.linalg.norm(
        query_embedding
    )

    document_norms = np.linalg.norm(
        document_embeddings,
        axis=1
    )

    denominator = (
        document_norms * query_norm
    )

    denominator = np.where(
        denominator == 0,
        1e-10,
        denominator
    )

    return np.dot(
        document_embeddings,
        query_embedding
    ) / denominator


# ============================================================
# LANGUAGE EXTRACTION
# ============================================================

def extract_language(
    text,
    language
):
    """
    Extract the requested language section
    from a multilingual document.
    """

    if language == "English":

        pattern = (
            r"English:\s*(.*?)"
            r"(?=\nHindi:|\nGujarati:|$)"
        )

    elif language == "Hindi":

        pattern = (
            r"Hindi:\s*(.*?)"
            r"(?=\nGujarati:|$)"
        )

    elif language == "Gujarati":

        pattern = (
            r"Gujarati:\s*(.*)$"
        )

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


# ============================================================
# LANGUAGE DETECTION
# ============================================================

def detect_language(query):
    """
    Detect Hindi, Gujarati or English.
    """

    hindi_count = len(
        re.findall(
            r"[\u0900-\u097F]",
            query
        )
    )

    gujarati_count = len(
        re.findall(
            r"[\u0A80-\u0AFF]",
            query
        )
    )

    if (
        hindi_count > 0
        and hindi_count >= gujarati_count
    ):
        return "Hindi"

    if gujarati_count > 0:
        return "Gujarati"

    return "English"


# ============================================================
# RETRIEVAL
# ============================================================

def retrieve(
    query,
    documents,
    bm25,
    document_embeddings,
    model
):
    """
    Retrieve documents using:

    BM25 + Dense Retrieval + Hybrid Ranking
    """

    # --------------------------------------------------------
    # BM25
    # --------------------------------------------------------

    query_tokens = tokenize(query)

    bm25_scores = bm25.get_scores(
        query_tokens
    )

    # --------------------------------------------------------
    # Dense Retrieval
    # --------------------------------------------------------

    query_embedding = model.encode(
        query,
        convert_to_numpy=True
    )

    dense_scores = cosine_similarity(
        query_embedding,
        document_embeddings
    )

    # --------------------------------------------------------
    # Normalize
    # --------------------------------------------------------

    bm25_scores = normalize(
        bm25_scores
    )

    dense_scores = normalize(
        dense_scores
    )

    # --------------------------------------------------------
    # Hybrid Score
    # --------------------------------------------------------

    hybrid_scores = (
        ALPHA * bm25_scores
        + (1 - ALPHA) * dense_scores
    )

    # --------------------------------------------------------
    # Ranking
    # --------------------------------------------------------

    ranked_indices = np.argsort(
        hybrid_scores
    )[::-1]

    return ranked_indices[:TOP_K]


# ============================================================
# LOAD FLAN-T5
# ============================================================

def load_generator():
    """
    Load FLAN-T5 using the correct
    sequence-to-sequence interface.
    """

    print("\nLoading FLAN-T5 generator...")

    tokenizer = AutoTokenizer.from_pretrained(
        GENERATOR_MODEL
    )

    model = AutoModelForSeq2SeqLM.from_pretrained(
        GENERATOR_MODEL
    )

    # Use GPU if available.
    device = torch.device(
        "cuda"
        if torch.cuda.is_available()
        else "cpu"
    )

    model = model.to(device)

    model.eval()

    print(
        f"Generator device: {device}"
    )

    return tokenizer, model, device


# ============================================================
# GENERATE ANSWER
# ============================================================

def generate_answer(
    query,
    context,
    language,
    tokenizer,
    model,
    device
):
    """
    Generate an answer using only retrieved evidence.
    """

    prompt = f"""
Answer the question using only the information
provided in the sources.

Do not invent information.
If the sources do not contain enough information,
say that the available sources do not provide
enough information.

Answer in {language}.

Question:
{query}

Sources:
{context}

Answer:
"""

    # --------------------------------------------------------
    # Tokenize prompt
    # --------------------------------------------------------

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=2048
    )

    inputs = {
        key: value.to(device)
        for key, value in inputs.items()
    }

    # --------------------------------------------------------
    # Generate
    # --------------------------------------------------------

    with torch.no_grad():

        output_ids = model.generate(
            **inputs,
            max_new_tokens=150,
            num_beams=4,
            do_sample=False,
            early_stopping=True
        )

    # --------------------------------------------------------
    # Decode
    # --------------------------------------------------------

    answer = tokenizer.decode(
        output_ids[0],
        skip_special_tokens=True
    )

    return answer.strip()


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print(
        "IndicSeek - Retrieval + RAG Generation"
    )
    print("=" * 70)

    # --------------------------------------------------------
    # Load documents
    # --------------------------------------------------------

    documents = load_documents()

    print(
        f"\nDocuments loaded: {len(documents)}"
    )

    if not documents:
        print(
            "\nERROR: No documents found."
        )
        print(
            f"Expected directory: {DOCUMENT_DIR}"
        )
        return

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
    # Load multilingual retriever
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
    # Create document embeddings
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
        "\nDocument embeddings created."
    )

    print(
        f"Embedding shape: "
        f"{document_embeddings.shape}"
    )

    # --------------------------------------------------------
    # Load generator
    # --------------------------------------------------------

    tokenizer, generator_model, device = (
        load_generator()
    )

    # --------------------------------------------------------
    # Query
    # --------------------------------------------------------

    print("\n" + "=" * 70)

    query = input(
        "\nEnter your query: "
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
    # Retrieve evidence
    # --------------------------------------------------------

    print(
        "\nRetrieving relevant documents..."
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
    # Display retrieved evidence
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
    # Build RAG context
    # --------------------------------------------------------

    context = ""

    for item in evidence:

        context += (
            f"\nSource {item['id']}:\n"
            f"{item['text']}\n"
        )

    # --------------------------------------------------------
    # Generate answer
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("GENERATING ANSWER...")
    print("=" * 70)

    answer = generate_answer(
        query,
        context,
        language,
        tokenizer,
        generator_model,
        device
    )

    # --------------------------------------------------------
    # Final output
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("FINAL ANSWER")
    print("=" * 70)

    print(
        f"\n{answer}"
    )

    print("\n" + "=" * 70)
    print("SOURCES")
    print("=" * 70)

    for item in evidence:

        print(
            f"{item['rank']}. {item['id']}"
        )

    print("\n" + "=" * 70)
    print("IndicSeek RAG completed.")
    print("=" * 70)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()