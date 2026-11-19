import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"

print("=" * 70)
print("IndicSeek - Cross-Lingual Generation Test")
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


def generate(question, evidence):

    messages = [
        {
            "role": "system",
            "content": """
You are an evidence-grounded question answering system.

Answer ONLY using the provided evidence.

Return the answer in ENGLISH.

Do not repeat the question.
Do not explain your reasoning.
Do not invent information.
Give only 1 short factual sentence.
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
            max_new_tokens=50,
            do_sample=False,
            repetition_penalty=1.1
        )

    generated = outputs[0][inputs["input_ids"].shape[1]:]

    return tokenizer.decode(
        generated,
        skip_special_tokens=True
    ).strip()


tests = [

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
    print(f"TEST {i}: {language} QUERY → ENGLISH ANSWER")
    print("=" * 70)

    print("\nQuestion:")
    print(question)

    print("\nEvidence:")
    print(evidence)

    answer = generate(question, evidence)

    print("\nGenerated English Answer:")
    print(answer)


print("\n" + "=" * 70)
print("CROSS-LINGUAL TEST COMPLETED")
print("=" * 70)