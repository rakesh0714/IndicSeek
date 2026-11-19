import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"

print("=" * 70)
print("IndicSeek - Qwen Multilingual Generator Test v2")
print("=" * 70)

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    dtype=torch.float32
)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)
model.eval()

print(f"Device: {device}")


def generate_answer(question, evidence, language):

    messages = [
        {
            "role": "system",
            "content": f"""
You are an evidence-grounded question answering system.

Rules:
1. Answer ONLY using the evidence.
2. Do not add information that is not present in the evidence.
3. Give a short answer of 1 or 2 sentences.
4. Answer ONLY in {language}.
5. Do not explain your reasoning.
6. Do not translate the question.
"""
        },
        {
            "role": "user",
            "content": f"""
Question:
{question}

Evidence:
{evidence}

Answer:
"""
        }
    ]

    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=1024
    ).to(device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=60,
            do_sample=False,
            repetition_penalty=1.1
        )

    generated_tokens = outputs[0][inputs["input_ids"].shape[1]:]

    answer = tokenizer.decode(
        generated_tokens,
        skip_special_tokens=True
    )

    return answer.strip()


tests = [

    (
        "English",
        "What documents are required for a scholarship application?",
        "Scholarship applications may require identity proof, academic records, bank account details, and an income certificate."
    ),

    (
        "Hindi",
        "छात्रवृत्ति के लिए कौन से दस्तावेज आवश्यक हैं?",
        "छात्रवृत्ति आवेदन के लिए पहचान प्रमाण, शैक्षणिक रिकॉर्ड, बैंक खाते की जानकारी और आय प्रमाण पत्र आवश्यक हो सकते हैं।"
    ),

    (
        "Gujarati",
        "શિષ્યવૃત્તિ માટે કયા દસ્તાવેજો જરૂરી છે?",
        "શિષ્યવૃત્તિ અરજી માટે ઓળખનો પુરાવો, શૈક્ષણિક રેકોર્ડ, બેંક ખાતાની વિગતો અને આવકનું પ્રમાણપત્ર જરૂરી હોઈ શકે છે."
    )
]


for i, (language, question, evidence) in enumerate(tests, 1):

    print("\n" + "=" * 70)
    print(f"TEST {i}: {language}")
    print("=" * 70)

    print("\nQuestion:")
    print(question)

    print("\nEvidence:")
    print(evidence)

    answer = generate_answer(
        question,
        evidence,
        language
    )

    print("\nGenerated Answer:")
    print(answer)


print("\n" + "=" * 70)
print("QWEN V2 TEST COMPLETED")
print("=" * 70)