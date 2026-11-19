import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

MODEL_NAME = "google/mt5-small"


def generate_answer(question, evidence, language, tokenizer, model, device):
    prompt = f"""
Answer the question using only the evidence.

Question:
{question}

Evidence:
{evidence}

Answer in {language}:
"""

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=512
    )

    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=100,
            num_beams=4,
            do_sample=False,
            early_stopping=True
        )

    answer = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    )

    return answer.strip()


print("=" * 70)
print("IndicSeek - mT5 Multilingual Generator Test")
print("=" * 70)

print("\nLoading mT5-small...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)
model.eval()

print(f"Device: {device}")


# ---------------------------------------------------------
# TEST 1: English
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("TEST 1: English")
print("=" * 70)

question = "What documents are required for a scholarship application?"

evidence = """
Scholarship applications may require identity proof,
academic records, bank account details, and an income certificate.
"""

answer = generate_answer(
    question,
    evidence,
    "English",
    tokenizer,
    model,
    device
)

print("\nQuestion:")
print(question)

print("\nGenerated Answer:")
print(answer)


# ---------------------------------------------------------
# TEST 2: Hindi
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("TEST 2: Hindi")
print("=" * 70)

question = "छात्रवृत्ति के लिए कौन से दस्तावेज आवश्यक हैं?"

evidence = """
छात्रवृत्ति आवेदन के लिए पहचान प्रमाण,
शैक्षणिक रिकॉर्ड, बैंक खाते की जानकारी
और आय प्रमाण पत्र आवश्यक हो सकते हैं।
"""

answer = generate_answer(
    question,
    evidence,
    "Hindi",
    tokenizer,
    model,
    device
)

print("\nQuestion:")
print(question)

print("\nGenerated Answer:")
print(answer)


# ---------------------------------------------------------
# TEST 3: Gujarati
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("TEST 3: Gujarati")
print("=" * 70)

question = "શિષ્યવૃત્તિ માટે કયા દસ્તાવેજો જરૂરી છે?"

evidence = """
શિષ્યવૃત્તિ અરજી માટે ઓળખનો પુરાવો,
શૈક્ષણિક રેકોર્ડ, બેંક ખાતાની વિગતો
અને આવકનું પ્રમાણપત્ર જરૂરી હોઈ શકે છે.
"""

answer = generate_answer(
    question,
    evidence,
    "Gujarati",
    tokenizer,
    model,
    device
)

print("\nQuestion:")
print(question)

print("\nGenerated Answer:")
print(answer)


print("\n" + "=" * 70)
print("mT5 GENERATOR TEST COMPLETED")
print("=" * 70)